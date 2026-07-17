# apps/faculty_attendance/models.py

from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class FacultyAttendance(TimeStampedModel):
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    is_present = models.BooleanField(default=True)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='faculty_attendances_marked')

    class Meta:
        unique_together = ('faculty', 'date')
        ordering = ['-date', 'faculty__first_name']

    def __str__(self):
        return f"{self.faculty.get_full_name()} - {self.date} - {'Present' if self.is_present else 'Absent'}"