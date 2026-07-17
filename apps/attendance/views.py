from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils import timezone
from django.db import transaction

from apps.core.mixins import FacultyRequiredMixin
from apps.academics.models import Subject, Batch, Enrollment
from .models import Attendance


class SelectSubjectForAttendanceView(FacultyRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return redirect("dashboard:faculty_dashboard")


class AttendanceDashboardView(FacultyRequiredMixin, View):
    template_name = "attendance/attendance_dashboard.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.role == "HOD":
            assigned_subjects = Subject.objects.all().order_by("name")
        else:
            assigned_subjects = Subject.objects.filter(
                faculty_mappings__faculty=user
            ).distinct()

        subject_id = request.GET.get("subject")
        batch_id = request.GET.get("batch")

        students = None
        subject = None
        batch = None

        if subject_id and batch_id:
            subject = get_object_or_404(Subject, pk=subject_id)
            batch = get_object_or_404(Batch, pk=batch_id)

            students = (
                Enrollment.objects.filter(batch=batch, is_active=True)
                .select_related("student__studentprofile")
                .order_by("student__first_name")
            )

            today = timezone.now().date()

            if Attendance.objects.filter(
                subject=subject,
                batch=batch,
                date=today,
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


class TakeAttendanceView(FacultyRequiredMixin, View):
    template_name = "attendance/take_attendance.html"

    def get(self, request, subject_id, batch_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        batch = get_object_or_404(Batch, pk=batch_id)

        students = (
            Enrollment.objects.filter(batch=batch, is_active=True)
            .select_related("student")
            .order_by("student__first_name")
        )

        today = timezone.now().date()

        existing_attendance = Attendance.objects.filter(
            subject=subject,
            batch=batch,
            date=today,
        )

        mode = request.GET.get("mode", "take")

        attendance_taken = existing_attendance.exists()

        if attendance_taken and mode != "edit":
            mode = "view"

        student_attendance_map = {
            attendance.student_id: attendance.is_present
            for attendance in existing_attendance
        }

        context = {
            "subject": subject,
            "batch": batch,
            "students": students,
            "mode": mode,
            "attendance_taken": attendance_taken,
            "student_attendance_map": student_attendance_map,
        }

        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, subject_id, batch_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        batch = get_object_or_404(Batch, pk=batch_id)

        student_ids = request.POST.getlist("student_id")
        present_students = request.POST.getlist("is_present")

        today = timezone.now().date()

        Attendance.objects.filter(
            subject=subject,
            batch=batch,
            date=today,
        ).delete()

        attendance_records = []

        for student_id in student_ids:
            attendance_records.append(
                Attendance(
                    student_id=int(student_id),
                    marked_by=request.user,
                    subject=subject,
                    batch=batch,
                    date=today,
                    is_present=(student_id in present_students),
                )
            )

        Attendance.objects.bulk_create(attendance_records)

        messages.success(
            request,
            f"Attendance for {subject.name} has been saved successfully.",
        )

        return redirect(request.path)