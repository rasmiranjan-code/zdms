# apps/threed_library/forms.py

from django import forms
from .models import ThreeDModel

class ThreeDModelForm(forms.ModelForm):
    class Meta:
        model = ThreeDModel
        fields = ['title', 'description', 'model_file', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'model_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'model_file': 'Please upload files in .glb or .gltf format for best compatibility.',
        }