# apps/students/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Avg, Count
from apps.core.mixins import HODRequiredMixin, StudentRequiredMixin
from .models import AlumniStory, StudentProfile
from .forms import AlumniStoryForm, StudentUpdateForm
from apps.accounts.models import User, FacultySubjectBatchMapping
from apps.academics.models import Enrollment, Subject
from apps.mcqs.models import StudentAttempt
from apps.attendance.models import Attendance
from apps.notices.models import Notice


class StudentDashboardView(StudentRequiredMixin, TemplateView):
    template_name = 'students/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user

        try:
            enrollment = Enrollment.objects.select_related('current_semester', 'batch').get(student=student, is_active=True)
            context['enrollment'] = enrollment
            context['subjects'] = Subject.objects.filter(semester=enrollment.current_semester)
        except Enrollment.DoesNotExist:
            context['enrollment'] = None
            context['subjects'] = []

        # Performance Stats
        mcq_attempts = StudentAttempt.objects.filter(student=student)
        context['total_mcq_attempts'] = mcq_attempts.count()
        context['mcq_accuracy'] = mcq_attempts.filter(is_correct=True).count() / context['total_mcq_attempts'] * 100 if context['total_mcq_attempts'] > 0 else 0

        # Attendance Stats
        attendance_records = Attendance.objects.filter(student=student)
        total_classes = attendance_records.count()
        attended_classes = attendance_records.filter(is_present=True).count()
        context['attendance_percentage'] = (attended_classes / total_classes * 100) if total_classes > 0 else 0

        # Other data
        context['latest_notice'] = Notice.objects.order_by('-created_at').first()
        context['recent_activities'] = StudentAttempt.objects.filter(student=student).select_related('question__subject').order_by('-created_at')[:3]

        return context


class StudentProfileView(StudentRequiredMixin, DetailView):
    model = User
    template_name = 'students/profile.html'
    context_object_name = 'student'  # Pass the user object as 'student' to the template

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the active enrollment for the student
        context['enrollment'] = Enrollment.objects.filter(student=self.request.user, is_active=True).first()
        return context


class MyFacultyView(StudentRequiredMixin, ListView):
    """Displays a list of faculty members assigned to the student's current subjects."""
    model = FacultySubjectBatchMapping
    template_name = 'students/my_faculty.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        try:
            enrollment = Enrollment.objects.get(student=self.request.user, is_active=True)
            self.current_semester = enrollment.current_semester
            subjects = Subject.objects.filter(semester=self.current_semester)
            return FacultySubjectBatchMapping.objects.filter(subject__in=subjects).select_related('subject', 'faculty').order_by('subject__name')
        except Enrollment.DoesNotExist:
            self.current_semester = None
            return FacultySubjectBatchMapping.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_semester'] = getattr(self, 'current_semester', None)
        return context


class StudentListView(HODRequiredMixin, ListView):
    model = User
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_queryset(self):
        return User.objects.filter(role='STUDENT').order_by('first_name', 'last_name')


class AlumniStoryListView(HODRequiredMixin, ListView):
    model = AlumniStory
    template_name = 'students/alumni_story_list.html'
    context_object_name = 'stories'
    paginate_by = 10


class AlumniStoryCreateView(HODRequiredMixin, CreateView):
    model = AlumniStory
    form_class = AlumniStoryForm
    template_name = 'students/alumni_story_form.html'
    success_url = reverse_lazy('students:alumni_story_list')

    def form_valid(self, form):
        messages.success(self.request, "Alumni story created successfully.")
        return super().form_valid(form)


class AlumniStoryUpdateView(HODRequiredMixin, UpdateView):
    model = AlumniStory
    form_class = AlumniStoryForm
    template_name = 'students/alumni_story_form.html'
    success_url = reverse_lazy('students:alumni_story_list')


class AlumniStoryDeleteView(HODRequiredMixin, DeleteView):
    model = AlumniStory
    template_name = 'students/alumni_story_confirm_delete.html'
    success_url = reverse_lazy('students:alumni_story_list')
    context_object_name = 'story'