from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.accounts.models import User


class StudentProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='studentprofile')
    college_roll_number = models.CharField(max_length=50, unique=True)
    university_roll_number = models.CharField(max_length=50, unique=True)
    # Add other student-specific fields here if needed

    def __str__(self):
        return f"{self.user.username} - {self.college_roll_number}"
    
class AlumniStory(TimeStampedModel):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="Select a student from an inactive/graduated batch.")
    photo = models.ImageField(upload_to='alumni_stories/')
    current_role = models.CharField(max_length=255, help_text="e.g., Wildlife Researcher, PhD Scholar")
    testimonial = models.TextField(blank=True)
    is_featured = models.BooleanField(default=True, help_text="Show this story on the landing page.")

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Alumni Stories"

    def __str__(self):
        return f"Success story of {self.student.get_full_name()}"
