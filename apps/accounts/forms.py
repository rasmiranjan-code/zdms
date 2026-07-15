# apps/accounts/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from apps.accounts.models import User
from apps.accounts.validators import validate_unique_username


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)


class StudentAccountCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        validate_unique_username(username)
        return username

    def save(self, commit=True, created_by=None):
        user = super().save(commit=False)
        user.role = 'STUDENT'
        user.set_password(self.cleaned_data['password'])
        user.created_by = created_by
        if commit:
            user.save()
        return user


class FacultyAccountCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        validate_unique_username(username)
        return username

    def save(self, commit=True, created_by=None):
        user = super().save(commit=False)
        user.role = 'FACULTY'
        user.set_password(self.cleaned_data['password'])
        user.created_by = created_by
        if commit:
            user.save()
        return user