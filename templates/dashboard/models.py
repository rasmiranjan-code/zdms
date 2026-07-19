# apps/threed_library/models.py

from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class ThreeDModel(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    model_file = models.FileField(upload_to='3d_models/', help_text="Upload .glb or .gltf files.")
    thumbnail = models.ImageField(upload_to='3d_thumbnails/', blank=True, null=True, help_text="Optional preview image.")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='uploaded_models')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title