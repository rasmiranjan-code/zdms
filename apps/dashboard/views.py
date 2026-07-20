# apps/dashboard/views.py
# This file can be used for more complex dashboard logic later.

from django.db.models import Count, Q
from django.views.generic import TemplateView
from apps.core.mixins import FacultyRequiredMixin, HODRequiredMixin
from apps.accounts.models import FacultySubjectBatchMapping, User
from apps.academics.models import Batch, Subject, Semester, Enrollment
from apps.mcqs.models import Question
from apps.notes.models import Note
from apps.attendance.models import Attendance
from apps.quiz.models import Quiz
from apps.mcqs.models import StudentAttempt
from apps.audit.models import AuditLog


class HODDashboardView(HODRequiredMixin, TemplateView):
    template_name = 'registration/hod_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_count'] = User.objects.filter(role='STUDENT').count()
        context['faculty_count'] = User.objects.filter(role='FACULTY').count()
        context['subject_count'] = Subject.objects.count()
        context['batch_count'] = Batch.objects.count()
        context['recent_activities'] = AuditLog.objects.select_related('actor').all()[:5]
        return context


class HODAnalyticsView(HODRequiredMixin, TemplateView):
    template_name = 'dashboard/hod_analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Overall Attendance
        total_classes = Attendance.objects.count()
        attended_classes = Attendance.objects.filter(is_present=True).count()
        context['overall_attendance'] = (attended_classes / total_classes * 100) if total_classes > 0 else 0

        # Overall MCQ Accuracy
        total_attempts = StudentAttempt.objects.count()
        correct_attempts = StudentAttempt.objects.filter(is_correct=True).count()
        context['overall_mcq_accuracy'] = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0

        context['total_mcqs'] = Question.objects.count()
        context['total_notes'] = Note.objects.count()

        # --- Chart Data ---
        batch_filter_id = self.request.GET.get('batch')
        
        # Batch-wise performance data for chart
        all_batches = Batch.objects.all().select_related('academic_session').order_by('-academic_session__start_year')
        
        batches_to_chart = all_batches
        if batch_filter_id:
            batches_to_chart = all_batches.filter(pk=batch_filter_id)

        batch_performance_data = []

        for batch in batches_to_chart:
            student_ids = batch.enrollments.filter(is_active=True).values_list('student_id', flat=True)

            batch_total_classes = Attendance.objects.filter(student_id__in=student_ids).count()
            batch_attended_classes = Attendance.objects.filter(student_id__in=student_ids, is_present=True).count()
            batch_attendance = (batch_attended_classes / batch_total_classes * 100) if batch_total_classes > 0 else 0
            batch_total_attempts = StudentAttempt.objects.filter(student_id__in=student_ids).count()
            batch_correct_attempts = StudentAttempt.objects.filter(student_id__in=student_ids, is_correct=True).count()
            batch_accuracy = (batch_correct_attempts / batch_total_attempts * 100) if batch_total_attempts > 0 else 0

            batch_performance_data.append({
                'name': str(batch.academic_session),
                'attendance': round(batch_attendance, 2),
                'accuracy': round(batch_accuracy, 2),
            })
        
        context['batch_performance_data'] = batch_performance_data
        context['all_batches'] = all_batches
        context['selected_batch'] = int(batch_filter_id) if batch_filter_id else None
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

        # --- Stats Calculation ---
        assigned_batch_ids = context['assigned_batches'].values_list('id', flat=True)

        # Total unique subjects and batches assigned
        context['assigned_subjects_count'] = assignments.values('subject').distinct().count()
        context['assigned_batches_count'] = assigned_batch_ids.count()

        # Total MCQs and Notes added by this faculty
        context['mcqs_added_count'] = Question.objects.filter(created_by=faculty).count()
        context['notes_added_count'] = Note.objects.filter(uploaded_by=faculty).count()

        # Total unique students in the faculty's assigned batches
        context['total_students'] = Enrollment.objects.filter(batch_id__in=assigned_batch_ids).values('student').distinct().count()

        # Total attendance sessions taken by the faculty
        context['attendance_taken'] = Attendance.objects.filter(marked_by=faculty).values('date', 'subject', 'batch').distinct().count()

        # Total tests created by the faculty
        context['tests_created'] = Quiz.objects.filter(created_by=faculty).count()

        return context