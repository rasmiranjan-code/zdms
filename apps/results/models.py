# apps/results/models.py

from django.db import models
from apps.core.models import TimeStampedModel
from django.conf import settings
from apps.academics.models import Subject, Semester

class Result(TimeStampedModel):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='results')
    internal_marks = models.PositiveIntegerField(default=0)
    external_marks = models.PositiveIntegerField(default=0)

    @property
    def total_marks(self):
        return self.internal_marks + self.external_marks

    def __str__(self):
        return f"Result for {self.student} in {self.subject}"

    class Meta:
        unique_together = ('student', 'subject', 'semester')
        ordering = ['semester__number', 'subject__name']