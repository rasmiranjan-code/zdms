# apps/mcqs/models.py

from django.db import models
from apps.core.models import TimeStampedModel
from apps.academics.models import Subject
from django.conf import settings


class Question(TimeStampedModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mcq_questions')
    question_text = models.TextField()
    image = models.ImageField(upload_to='mcq_images/', blank=True, null=True)

    def __str__(self):
        return self.question_text[:100]

    class Meta:
        ordering = ['created_at']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text

    class Meta:
        ordering = ['?'] # Randomize answer order by default


class QuestionEditHistory(TimeStampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='edit_history')
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mcq_edits')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Question Edit Histories"


class StudentAttempt(TimeStampedModel):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mcq_attempts')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='attempts')
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='attempts')
    is_correct = models.BooleanField()

    class Meta:
        ordering = ['-created_at']
