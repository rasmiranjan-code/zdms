# apps/threed_library/forms.py

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

    def clean_model_file_glb(self):
        model_file = self.cleaned_data.get('model_file_glb', False)
        if model_file:
            ext = os.path.splitext(model_file.name)[1]
            valid_extensions = ['.glb']
            if not ext.lower() in valid_extensions:
                raise forms.ValidationError('Unsupported file type. Please upload a .glb file for the viewer.')
        return model_file