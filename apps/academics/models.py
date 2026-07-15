# apps/academics/models.py

from django.db import models
from apps.core.models import TimeStampedModel
from apps.core.constants import SEMESTER_STATUS_CHOICES, SUBJECT_TYPE_CHOICES
from django.conf import settings


class AcademicSession(TimeStampedModel):
    """Represents an academic session, e.g., 2025-2026."""
    start_year = models.PositiveIntegerField(default=2024)
    end_year = models.PositiveIntegerField(default=2025)

    def __str__(self):
        return f"{self.start_year}-{self.end_year}"

    class Meta:
        ordering = ['-start_year']
        unique_together = ('start_year', 'end_year')


class Batch(TimeStampedModel):
    """Represents a group of students, e.g., B.Sc. Zoology 2024-2027."""
    academic_session = models.OneToOneField(AcademicSession, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.academic_session)


class Semester(TimeStampedModel):
    """Represents a semester within a batch."""
    number = models.CharField(max_length=20)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='semesters')
    status = models.CharField(max_length=20, choices=SEMESTER_STATUS_CHOICES, default='UPCOMING')

    class Meta:
        unique_together = ('batch', 'number')

    def __str__(self):
        return f"Semester {self.number} - {self.batch}"


class Subject(TimeStampedModel):
    """Represents a course or subject."""
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    subject_type = models.CharField(max_length=10, choices=SUBJECT_TYPE_CHOICES, default='THEORY')

    def __str__(self):
        return f"{self.name} ({self.code})"


class Enrollment(TimeStampedModel):
    """Links a student to a batch and their current semester."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='enrollments')
    current_semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='current_enrollments')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'batch')

    def __str__(self):
        return f"{self.student.username} in {self.batch}"