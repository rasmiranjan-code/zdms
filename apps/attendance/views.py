# apps/attendance/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils import timezone
from apps.core.mixins import FacultyRequiredMixin
from apps.academics.models import Subject, Batch, Enrollment
from .models import Attendance


class SelectSubjectForAttendanceView(FacultyRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # This view is now part of the FacultyDashboardView
        # Redirecting to the dashboard
        return redirect('dashboard:faculty_dashboard')


class TakeAttendanceView(FacultyRequiredMixin, View):
    template_name = 'attendance/take_attendance.html'

    def get(self, request, subject_id, batch_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        batch = get_object_or_404(Batch, pk=batch_id)
        students = Enrollment.objects.filter(batch=batch, is_active=True).select_related('student').order_by('student__first_name')
        
        # Check if attendance for today is already taken
        today = timezone.now().date()
        if Attendance.objects.filter(subject=subject, batch=batch, date=today).exists():
            messages.info(request, f"Attendance for {subject.name} has already been taken today.")
            return redirect('dashboard:faculty_dashboard')

        context = {
            'subject': subject,
            'batch': batch,
            'students': students,
        }
        return render(request, self.template_name, context)

    def post(self, request, subject_id, batch_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        batch = get_object_or_404(Batch, pk=batch_id)
        student_ids = request.POST.getlist('student_id')
        present_students = request.POST.getlist('is_present')
        today = timezone.now().date()

        attendance_records = []
        for student_id in student_ids:
            is_present = student_id in present_students
            attendance_records.append(
                Attendance(
                    student_id=int(student_id),
                    marked_by=request.user,
                    subject=subject,
                    batch=batch,
                    date=today,
                    is_present=is_present
                )
            )
        Attendance.objects.bulk_create(attendance_records)
        messages.success(request, f"Attendance for {subject.name} submitted successfully.")
        return redirect('dashboard:faculty_dashboard')