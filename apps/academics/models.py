# apps/academics/models.py

from django.db import models
from apps.core.models import TimeStampedModel
from apps.core.constants import SEMESTER_STATUS_CHOICES, SUBJECT_TYPE_CHOICES


class AcademicSession(TimeStampedModel):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Batch(TimeStampedModel):
    name = models.CharField(max_length=50)
    admission_year = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=(('ACTIVE', 'Active'), ('GRADUATING', 'Graduating'), ('ARCHIVED', 'Archived')),
        default='ACTIVE'
    )

    def __str__(self):
        return self.name


class Semester(TimeStampedModel):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='semesters')
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='semesters')
    number = models.IntegerField()
    status = models.CharField(max_length=20, choices=SEMESTER_STATUS_CHOICES, default='UPCOMING')

    class Meta:
        unique_together = ('batch', 'number')

    def __str__(self):
        return f"{self.batch} - Sem {self.number}"


class Subject(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPE_CHOICES, default='THEORY')
    credit = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(TimeStampedModel):
    student = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='enrollments')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='enrollments')
    current_semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, related_name='enrolled_students')

    class Meta:
        unique_together = ('student', 'batch')

    def __str__(self):
        return f"{self.student} - {self.batch}"