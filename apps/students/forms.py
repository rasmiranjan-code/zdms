# apps/students/forms.py

from django import forms
from django.db import transaction
from .models import AlumniStory
from apps.accounts.models import User
from apps.academics.models import Batch, Semester, Enrollment
from .models import StudentProfile


class StudentUpdateForm(forms.ModelForm):
    college_roll_number = forms.CharField(max_length=50, required=True)
    university_roll_number = forms.CharField(max_length=50, required=True)
    batch = forms.ModelChoiceField(queryset=Batch.objects.all(), required=True, disabled=True)
    current_semester = forms.ModelChoiceField(queryset=Semester.objects.none(), required=True, disabled=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply form-control class to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        if self.instance and self.instance.pk:
            try:
                self.fields['college_roll_number'].initial = self.instance.studentprofile.college_roll_number
                self.fields['university_roll_number'].initial = self.instance.studentprofile.university_roll_number
                enrollment = self.instance.enrollments.get(is_active=True)
                self.fields['batch'].initial = enrollment.batch
                if enrollment.batch:
                    self.fields['current_semester'].queryset = Semester.objects.filter(batch=enrollment.batch)
                self.fields['current_semester'].initial = enrollment.current_semester
            except (StudentProfile.DoesNotExist, Enrollment.DoesNotExist, Enrollment.MultipleObjectsReturned):
                pass

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)
        # StudentProfile is linked to user, so we update it.
        # We don't create it here as it's created on student registration.
        if hasattr(user, 'studentprofile'):
            profile = user.studentprofile
            profile.college_roll_number = self.cleaned_data['college_roll_number']
            profile.university_roll_number = self.cleaned_data['university_roll_number']
            if commit:
                profile.save()
        
        # Batch and semester are not editable by the student.

        return user


class AlumniStoryForm(forms.ModelForm):
    class Meta:
        model = AlumniStory
        fields = ['student_name', 'batch_year', 'photo', 'current_role', 'testimonial', 'is_featured']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})