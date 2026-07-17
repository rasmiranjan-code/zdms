# apps/academics/views.py

from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, CreateView
from .models import AcademicSession, Batch, Semester, Subject
from .forms import AcademicSessionForm, BatchForm, SemesterForm, SubjectForm
from apps.core.mixins import HODRequiredMixin


class AcademicSessionListView(HODRequiredMixin, ListView):
    model = AcademicSession
    template_name = 'academics/session_list.html'
    context_object_name = 'sessions'


class AcademicSessionCreateView(HODRequiredMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = 'academics/session_form.html'
    success_url = reverse_lazy('academics:session_list')


class BatchListView(HODRequiredMixin, ListView):
    model = Batch
    template_name = 'academics/batch_list.html'
    context_object_name = 'batches'


class BatchCreateView(HODRequiredMixin, CreateView):
    model = Batch
    form_class = BatchForm
    template_name = 'academics/batch_form.html'
    success_url = reverse_lazy('academics:batch_list')


class SemesterListView(HODRequiredMixin, ListView):
    model = Semester
    template_name = 'academics/semester_list.html'
    context_object_name = 'semesters'


class SemesterCreateView(HODRequiredMixin, CreateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'academics/semester_form.html'
    success_url = reverse_lazy('academics:semester_list')


class SubjectListView(HODRequiredMixin, ListView):
    model = Subject
    template_name = 'academics/subject_list.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        return Subject.objects.select_related('semester__batch__academic_session').all()


class SubjectCreateView(HODRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'academics/subject_form.html'
    success_url = reverse_lazy('academics:subject_list')


def get_semesters_for_batch(request):
    batch_id = request.GET.get('batch_id')
    semesters = Semester.objects.filter(batch_id=batch_id).order_by('number')
    return JsonResponse(list(semesters.values('id', 'number')), safe=False)


def get_batches_for_subject(request):
    subject_id = request.GET.get('subject_id')
    user = request.user

    if user.role == 'HOD':
        # HOD can see all batches for a subject
        batches = Batch.objects.filter(semesters__subjects__id=subject_id).distinct().select_related('academic_session')
    else: # Faculty
        # Faculty sees only batches assigned to them for that subject
        batches = Batch.objects.filter(
            faculty_mappings__subject_id=subject_id,
            faculty_mappings__faculty=user
        ).distinct().select_related('academic_session')
    return JsonResponse([{'id': batch.id, 'name': str(batch.academic_session)} for batch in batches], safe=False)