# apps/accounts/validators.py

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


def validate_unique_roll_number(roll_number):
    from apps.students.models import StudentProfile
    if StudentProfile.objects.filter(roll_number=roll_number).exists():
        raise ValidationError('A student with this roll number already exists.')


def validate_unique_username(username):
    User = get_user_model()
    if User.objects.filter(username=username).exists():
        raise ValidationError('This username is already taken.')