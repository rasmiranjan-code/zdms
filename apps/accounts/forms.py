# apps/accounts/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from apps.academics.models import Batch, Semester, Enrollment, Subject
from apps.students.models import StudentProfile

User = get_user_model()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class StudentAccountCreationForm(forms.ModelForm):
    college_roll_number = forms.CharField(max_length=50, required=True)
    university_roll_number = forms.CharField(max_length=50, required=True)
    batch = forms.ModelChoiceField(queryset=Batch.objects.all(), required=True)
    current_semester = forms.ModelChoiceField(queryset=Semester.objects.none(), required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'profile_picture')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        if 'batch' in self.data:
            try:
                batch_id = int(self.data.get('batch'))
                self.fields['current_semester'].queryset = Semester.objects.filter(batch_id=batch_id).order_by('number')
            except (ValueError, TypeError):
                pass  # invalid input from a user; validation will fail on the form

    @transaction.atomic
    def save(self, commit=True, created_by=None):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = 'STUDENT'
        if created_by:
            user.created_by = created_by
        
        if commit:
            user.save()
            # Create StudentProfile
            StudentProfile.objects.create(
                user=user,
                college_roll_number=self.cleaned_data['college_roll_number'],
                university_roll_number=self.cleaned_data['university_roll_number']
            )
            # Create Enrollment
            Enrollment.objects.create(
                student=user,
                batch=self.cleaned_data['batch'],
                current_semester=self.cleaned_data['current_semester'],
                is_active=True
            )
        return user


class StudentUpdateForm(forms.ModelForm):
    college_roll_number = forms.CharField(max_length=50, required=True)
    university_roll_number = forms.CharField(max_length=50, required=True)
    batch = forms.ModelChoiceField(queryset=Batch.objects.all(), required=True)
    current_semester = forms.ModelChoiceField(queryset=Semester.objects.none(), required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply form-control class to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        if 'batch' in self.data:
            try:
                batch_id = int(self.data.get('batch'))
                self.fields['current_semester'].queryset = Semester.objects.filter(batch_id=batch_id).order_by('number')
            except (ValueError, TypeError):
                pass

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
        StudentProfile.objects.update_or_create(
            user=user,
            defaults={
                'college_roll_number': self.cleaned_data['college_roll_number'],
                'university_roll_number': self.cleaned_data['university_roll_number'],
            }
        )
        Enrollment.objects.update_or_create(
            student=user, is_active=True,
            defaults={
                'batch': self.cleaned_data['batch'],
                'current_semester': self.cleaned_data['current_semester'],
            }
        )
        return user


class FacultyAssignForm(forms.Form):
    faculty = forms.ModelChoiceField(
        queryset=User.objects.filter(role='FACULTY'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all().select_related('semester__batch__academic_session'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].label_from_instance = lambda obj: f"{obj.name} ({obj.code}) - {obj.semester}"


class FacultyAccountCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'profile_picture', 'specialization')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True, created_by=None):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = 'FACULTY'
        if created_by:
            user.created_by = created_by
        if commit:
            user.save()
        return user


class HODProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class FacultyUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'specialization')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class FacultyPasswordChangeForm(forms.Form):
    new_password = forms.CharField(                                                                                  
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if self.user and self.user.check_password(new_password):
            raise forms.ValidationError(
                "New Password cannot be the same as the old password."
            )
        return new_password