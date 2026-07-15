from django.db import models
from apps.core.models import TimeStampedModel
from apps.academics.models import Subject, Batch


class Attendance(TimeStampedModel):
    student = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='attendance_records'
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
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attendance_marked'
    )

    class Meta:
        unique_together = ('student', 'subject', 'date')
        ordering = ['-date']

    def __str__(self):
        status = 'Present' if self.is_present else 'Absent'
        return f"{self.student} - {self.subject} - {self.date} - {status}"