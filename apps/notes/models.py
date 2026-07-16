# apps/notes/models.py

from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.academics.models import Subject

class Note(TimeStampedModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='notes/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_notes')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']