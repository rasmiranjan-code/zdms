# d:/zdms/apps/threed_library/forms.py

import os
from django import forms
from .models import ThreeDModel

class ThreeDModelForm(forms.ModelForm):
    class Meta:
        model = ThreeDModel
        fields = ['title', 'description', 'thumbnail', 'model_file_glb', 'model_file_gltf', 'model_file_usdz', 'model_file_fbx']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'model_file_glb': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'model_file_gltf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'model_file_usdz': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'model_file_fbx': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'model_file_glb': 'This .glb file will be used for the interactive web viewer.',
        }

    def _validate_file_extension(self, file, valid_extensions):
        """Helper function to validate file extension."""
        if file:
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(f'Unsupported file type. Please upload a file with one of the following extensions: {", ".join(valid_extensions)}')
        return file

    def clean_model_file_glb(self):
        return self._validate_file_extension(self.cleaned_data.get('model_file_glb'), ['.glb'])

    def clean_model_file_gltf(self):
        return self._validate_file_extension(self.cleaned_data.get('model_file_gltf'), ['.gltf'])

    def clean_model_file_usdz(self):
        return self._validate_file_extension(self.cleaned_data.get('model_file_usdz'), ['.usdz'])

    def clean_model_file_fbx(self):
        return self._validate_file_extension(self.cleaned_data.get('model_file_fbx'), ['.fbx'])
