from django.db import models
from apps.core.models import TimeStampedModel
from apps.accounts.models import User


class StudentProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='studentprofile')
    college_roll_number = models.CharField(max_length=50, unique=True)
    university_roll_number = models.CharField(max_length=50, unique=True)
    # Add other student-specific fields here if needed

    def __str__(self):
        return f"{self.user.username} - {self.college_roll_number}"
