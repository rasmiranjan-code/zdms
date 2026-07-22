# apps/attendance/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.db import transaction

from apps.core.mixins import HODFacultyRequiredMixin, StudentRequiredMixin
from apps.academics.models import Subject, Batch, Enrollment
from .models import Attendance


class SelectSubjectForAttendanceView(HODFacultyRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return redirect('dashboard:faculty_dashboard')


class AttendanceDashboardView(HODFacultyRequiredMixin, View):
    template_name = 'attendance/attendance_dashboard.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.role == 'HOD':
            assigned_subjects = Subject.objects.all().order_by('name')
        else:
            assigned_subjects = (
                Subject.objects
                .filter(faculty_mappings__faculty=user)
                .distinct()
                .order_by('name')
            )

        subject_id = request.GET.get('subject')
        batch_id = request.GET.get('batch')

        students = None
        subject = None
        batch = None

        if subject_id and batch_id:
            subject = get_object_or_404(Subject, pk=subject_id)
            batch = get_object_or_404(Batch, pk=batch_id)

            students = (
                Enrollment.objects
                .filter(batch=batch, is_active=True)
                .select_related('student__studentprofile')
                .order_by('student__first_name')
            )

            today = timezone.now().date()

            if Attendance.objects.filter(
                subject=subject,
                batch=batch,
                date=today
            ).exists():

                messages.info(
                    request,
                    f"Attendance for {subject.name} ({batch}) has already been taken today."
                )

        context = {
            "assigned_subjects": assigned_subjects,
            "students": students,
            "selected_subject": subject,
            "selected_batch": batch,
        }

        return render(request, self.template_name, context)


# ==========================
# STUDENT ATTENDANCE REPORT
# ==========================

class StudentAttendanceView(StudentRequiredMixin, View):
    template_name = "attendance/attendance.html"

    def get(self, request, *args, **kwargs):
        student = request.user

        attendance_records = []
        overall_total = 0
        overall_present = 0

        # Student ke saare attendance records
        records = (
            Attendance.objects
            .filter(student=student)
            .select_related("subject")
            .order_by("subject__name")
        )

        # Unique subjects
        subjects = records.values_list("subject_id", flat=True).distinct()

        for subject_id in subjects:

            subject_records = records.filter(subject_id=subject_id)

            subject = subject_records.first().subject

            total = subject_records.count()
            attended = subject_records.filter(is_present=True).count()

            percentage = (attended / total * 100) if total > 0 else 0

            attendance_records.append({
                "subject": subject.name,
                "total": total,
                "attended": attended,
                "percentage": round(percentage, 2),
            })

            overall_total += total
            overall_present += attended

        overall_percentage = (
            round((overall_present / overall_total) * 100, 2)
            if overall_total > 0 else 0
        )

        context = {
            "attendance_records": attendance_records,
            "overall_percentage": overall_percentage,
        }

        return render(request, self.template_name, context)

class TakeAttendanceView(HODFacultyRequiredMixin, View):

    template_name = "attendance/take_attendance.html"

    def get(self, request, subject_id, batch_id):

        subject = get_object_or_404(
            Subject,
            pk=subject_id
        )

        batch = get_object_or_404(
            Batch,
            pk=batch_id
        )

        students = (
            Enrollment.objects
            .filter(
                batch=batch,
                is_active=True
            )
            .select_related("student")
            .order_by("student__first_name")
        )

        today = timezone.now().date()

        existing_attendance = Attendance.objects.filter(
            subject=subject,
            batch=batch,
            date=today
        )

        attendance_taken = existing_attendance.exists()

        mode = request.GET.get("mode", "take")

        if attendance_taken and mode != "edit":
            mode = "view"

        student_attendance_map = {
            att.student_id: att.is_present
            for att in existing_attendance
        }

        context = {
            "subject": subject,
            "batch": batch,
            "students": students,
            "mode": mode,
            "attendance_taken": attendance_taken,
            "student_attendance_map": student_attendance_map,
        }

        return render(
            request,
            self.template_name,
            context
        )

    @transaction.atomic
    def post(self, request, subject_id, batch_id):

        subject = get_object_or_404(
            Subject,
            pk=subject_id
        )

        batch = get_object_or_404(
            Batch,
            pk=batch_id
        )

        today = timezone.now().date()

        Attendance.objects.filter(
            subject=subject,
            batch=batch,
            date=today
        ).delete()

        attendance_records = []

        present_students = set(
            request.POST.getlist("is_present")
        )

        for student_id in request.POST.getlist("student_id"):

            attendance_records.append(

                Attendance(
                    student_id=int(student_id),
                    subject=subject,
                    batch=batch,
                    marked_by=request.user,
                    date=today,
                    is_present=student_id in present_students,
                )

            )

        Attendance.objects.bulk_create(
            attendance_records
        )

        messages.success(
            request,
            "Attendance saved successfully."
        )

        return redirect(request.path)