# apps/accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel
from apps.core.constants import ROLE_CHOICES
from apps.accounts.managers import UserManager


class User(AbstractUser, TimeStampedModel):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    created_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='created_users'
    )

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"


class FacultySubjectBatchMapping(TimeStampedModel):
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subject_mappings')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='faculty_mappings')
    batch = models.ForeignKey('academics.Batch', on_delete=models.CASCADE, related_name='faculty_mappings')

    class Meta:
        unique_together = ('faculty', 'subject', 'batch')

    def __str__(self):
        return f"{self.faculty} - {self.subject} - {self.batch}"


class ClassCoordinatorAssignment(TimeStampedModel):
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coordinator_assignments')
    batch = models.ForeignKey('academics.Batch', on_delete=models.CASCADE, related_name='coordinators')

    class Meta:
        unique_together = ('faculty', 'batch')

    def __str__(self):
        return f"{self.faculty} - Coordinator - {self.batch}"