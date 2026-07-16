# apps/mcqs/models.py

from django.db import models
from apps.core.models import TimeStampedModel
from apps.academics.models import Subject
from django.conf import settings


class Question(TimeStampedModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mcq_questions')
    question_text = models.TextField()

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