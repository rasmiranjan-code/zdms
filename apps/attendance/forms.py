# apps/attendance/forms.py

from django import forms
from .models import Attendance

class TakeAttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['is_present']
        widgets = {
            'is_present': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }