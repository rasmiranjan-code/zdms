from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.academics.models import Subject, Batch


class Attendance(TimeStampedModel):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_attendances'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='marked_attendances'
    )

    def __str__(self):
        return f"Attendance for {self.student} in {self.subject} on {self.date}"