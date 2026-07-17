# apps/dashboard/views.py
# This file can be used for more complex dashboard logic later.

from django.views.generic import TemplateView
from apps.core.mixins import FacultyRequiredMixin, HODRequiredMixin
from apps.accounts.models import FacultySubjectBatchMapping, User
from apps.academics.models import Batch, Subject
from apps.mcqs.models import Question
from apps.notes.models import Note


class HODDashboardView(HODRequiredMixin, TemplateView):
    template_name = 'registration/hod_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_count'] = User.objects.filter(role='STUDENT').count()
        context['faculty_count'] = User.objects.filter(role='FACULTY').count()
        context['subject_count'] = Subject.objects.count()
        context['batch_count'] = Batch.objects.count()
        return context


class FacultyDashboardView(FacultyRequiredMixin, TemplateView):
    template_name = 'dashboard/faculty_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faculty = self.request.user
        batch_filter_id = self.request.GET.get('batch')

        # Get subjects assigned to the logged-in faculty member
        assignments = FacultySubjectBatchMapping.objects.filter(faculty=faculty).select_related(
            'subject', 'batch__academic_session'
        ).order_by('batch__academic_session__start_year', 'subject__name')

        if batch_filter_id:
            assignments = assignments.filter(batch_id=batch_filter_id)

        context['assignments'] = assignments
        # For filter dropdown
        context['assigned_batches'] = Batch.objects.filter(id__in=FacultySubjectBatchMapping.objects.filter(faculty=faculty).values_list('batch_id', flat=True).distinct())
        context['selected_batch'] = int(batch_filter_id) if batch_filter_id else None

        # Add stats for the dashboard
        distinct_subjects = assignments.values('subject').distinct()
        context['assigned_subjects_count'] = distinct_subjects.count()
        context['assigned_batches_count'] = assignments.values('batch').distinct().count()
        context['mcqs_added_count'] = Question.objects.filter(created_by=faculty).count()
        context['notes_added_count'] = Note.objects.filter(uploaded_by=faculty).count()
        return context