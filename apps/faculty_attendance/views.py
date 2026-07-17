from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from apps.core.mixins import HODRequiredMixin
from apps.accounts.models import User
from .models import FacultyAttendance

class TakeFacultyAttendanceView(HODRequiredMixin, View):
    template_name = 'faculty_attendance/take_attendance.html'

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        
        # Check if attendance has already been taken today
        existing_attendance = FacultyAttendance.objects.filter(date=today)
        
        if existing_attendance.exists():
            messages.info(request, "Faculty attendance has already been marked for today.")
            # Prepare context for viewing existing attendance
            faculty_attendance_map = {att.faculty_id: att.is_present for att in existing_attendance}
            faculties = User.objects.filter(role='FACULTY').order_by('first_name')
            context = {
                'faculties': faculties,
                'attendance_taken': True,
                'faculty_attendance_map': faculty_attendance_map,
                'date': today,
            }
        else:
            # Prepare context for taking new attendance
            faculties = User.objects.filter(role='FACULTY').order_by('first_name')
            context = {
                'faculties': faculties,
                'attendance_taken': False,
                'date': today,
            }
            
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        today = timezone.now().date()
        faculty_ids = request.POST.getlist('faculty_id')
        present_faculty_ids = request.POST.getlist('is_present')

        # Delete any existing records for today to prevent duplicates
        FacultyAttendance.objects.filter(date=today).delete()

        for faculty_id in faculty_ids:
            is_present = faculty_id in present_faculty_ids
            FacultyAttendance.objects.create(faculty_id=int(faculty_id), date=today, is_present=is_present, marked_by=request.user)

        messages.success(request, "Faculty attendance has been successfully recorded.")
        return redirect('faculty_attendance:take_attendance')
