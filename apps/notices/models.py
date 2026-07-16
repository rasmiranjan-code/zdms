from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class Notice(TimeStampedModel):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='notices/')
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_notices')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
