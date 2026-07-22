# apps/accounts/views.py

from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, FormView, ListView, UpdateView, DetailView
from apps.accounts.forms import LoginForm, StudentAccountCreationForm, FacultyAssignForm, FacultyAccountCreationForm, HODProfileUpdateForm, FacultyUpdateForm, FacultyPasswordChangeForm
from apps.audit.services import log_action
from apps.audit.models import AuditLog
from apps.core.mixins import HODRequiredMixin
from .models import FacultySubjectBatchMapping, User
from apps.students.models import StudentProfile, AlumniStory
from apps.notices.models import Notice
from apps.core.models import GalleryImage


class LandingPageView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == 'HOD':
                return redirect('dashboard:hod_dashboard')
            elif request.user.role == 'STUDENT':
                return redirect('students:dashboard')
            elif request.user.role == 'FACULTY':
                return redirect('dashboard:faculty_dashboard') # Corrected redirect for faculty
            # Add other roles here in the future
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Stats
        context['student_count'] = User.objects.filter(role='STUDENT', is_active=True).count()
        context['faculty_count'] = User.objects.filter(role__in=['FACULTY', 'HOD'], is_active=True).count()

        # Faculty List (HOD first, then others)
        hod = User.objects.filter(role='HOD').first()
        other_faculty = User.objects.filter(role='FACULTY').order_by('?')[:5]
        context['faculty_list'] = [hod] + list(other_faculty) if hod else list(other_faculty)

        # Alumni List (Students from inactive batches)
        context['alumni_stories'] = AlumniStory.objects.filter(is_featured=True)

        # Latest Notices
        context['latest_notices'] = Notice.objects.all().order_by('-created_at')[:3]

        # Gallery Images
        context['gallery_images'] = GalleryImage.objects.all().order_by('-created_at')[:9]
        return context


class HODCreateStudentView(HODRequiredMixin, CreateView):
    form_class = StudentAccountCreationForm
    template_name = 'accounts/hod_add_student.html'
    success_url = reverse_lazy('students:list')

    def form_valid(self, form):
        form.save(created_by=self.request.user)
        return super().form_valid(form)


class HODCreateFacultyView(HODRequiredMixin, CreateView):
    form_class = FacultyAccountCreationForm
    template_name = 'accounts/hod_add_faculty.html'
    success_url = reverse_lazy('accounts:faculty_assignment_list')

    def form_valid(self, form):
        form.save(created_by=self.request.user)
        return super().form_valid(form)


class HODSettingsView(HODRequiredMixin, UpdateView):
    model = User
    form_class = HODProfileUpdateForm
    template_name = 'accounts/hod_settings.html'
    success_url = reverse_lazy('accounts:hod_settings')

    def get_object(self, queryset=None):
        return self.request.user
    # Note: Logging for UpdateView is more complex, will add later if needed.


class FacultyDetailView(HODRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/faculty_detail.html'
    context_object_name = 'faculty'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignments'] = FacultySubjectBatchMapping.objects.filter(
            faculty=self.get_object()
        ).select_related('subject', 'batch__academic_session')
        return context


class FacultyUpdateView(HODRequiredMixin, UpdateView):
    model = User
    form_class = FacultyUpdateForm
    template_name = 'accounts/faculty_edit_form.html'

    def get_success_url(self):
        return reverse_lazy('accounts:faculty_detail', kwargs={'pk': self.object.pk})


class FacultyPasswordChangeView(HODRequiredMixin, FormView):
    form_class = FacultyPasswordChangeForm
    template_name = 'accounts/faculty_password_change.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faculty'] = User.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        faculty = User.objects.get(pk=self.kwargs['pk'])
        faculty.set_password(form.cleaned_data['new_password'])
        faculty.save()
        return redirect(reverse('accounts:faculty_detail', kwargs={'pk': faculty.pk}))


class RoleBasedLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'HOD':
                return reverse_lazy('dashboard:hod_dashboard')
            elif user.role == 'FACULTY':
                return reverse_lazy('dashboard:faculty_dashboard')
            elif user.role == 'STUDENT':
                return reverse_lazy('students:dashboard')
        return reverse_lazy('accounts:landing')


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # Clear all audit logs before logging out
        AuditLog.objects.all().delete()
        return super().dispatch(request, *args, **kwargs)


class FacultyAssignmentListView(HODRequiredMixin, ListView):
    model = FacultySubjectBatchMapping
    template_name = 'accounts/faculty_assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        return FacultySubjectBatchMapping.objects.select_related(
            'faculty', 'subject__semester__batch__academic_session'
        ).order_by('faculty__first_name', 'subject__name')


class FacultyAssignView(HODRequiredMixin, FormView):
    form_class = FacultyAssignForm
    template_name = 'accounts/faculty_assign_form.html'
    success_url = reverse_lazy('accounts:faculty_assignment_list')

    def form_valid(self, form):
        faculty = form.cleaned_data['faculty']
        subject = form.cleaned_data['subject']
        mapping, created = FacultySubjectBatchMapping.objects.get_or_create(
            faculty=faculty,
            subject=subject,
            batch=subject.semester.batch  # Automatically derive batch from subject
        )
        if created:
            log_action(actor=self.request.user, action="ASSIGNED_SUBJECT_TO_FACULTY", target=mapping)
        return super().form_valid(form)