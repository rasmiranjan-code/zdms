# apps/students/forms.py

from django import forms
from .models import AlumniStory
from apps.accounts.models import User


class AlumniStoryForm(forms.ModelForm):
    class Meta:
        model = AlumniStory
        fields = ['student_name', 'batch_year', 'photo', 'current_role', 'testimonial', 'is_featured']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})