# apps/threed_library/models.py

from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel

class ThreeDModel(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='3d_thumbnails/', blank=True, null=True, help_text="Optional preview image.")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='uploaded_models')

    # File fields for different formats
    model_file_glb = models.FileField(upload_to='3d_models/glb/', help_text="Viewer file (.glb format recommended)", blank=True, null=True)
    model_file_gltf = models.FileField(upload_to='3d_models/gltf/', help_text="Converted .gltf format", blank=True, null=True)
    model_file_usdz = models.FileField(upload_to='3d_models/usdz/', help_text="Converted .usdz format (for AR on Apple devices)", blank=True, null=True)
    model_file_fbx = models.FileField(upload_to='3d_models/fbx/', help_text="Original .fbx format", blank=True, null=True)

    def __str__(self):
        return self.title