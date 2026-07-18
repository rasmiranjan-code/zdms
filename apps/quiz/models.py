# apps/quiz/models.py

from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.academics.models import Subject
from apps.mcqs.models import Question, Answer

class Quiz(TimeStampedModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)
    duration_minutes = models.PositiveIntegerField(help_text="Duration of the quiz in minutes")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_marks = models.PositiveIntegerField(default=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False, help_text="Students can only see published quizzes.")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_time']
        verbose_name_plural = "Quizzes"

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('quiz', 'question')

class StudentQuizAttempt(TimeStampedModel):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    is_submitted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'quiz')

class StudentAnswer(TimeStampedModel):
    attempt = models.ForeignKey(StudentQuizAttempt, on_delete=models.CASCADE, related_name='answers')
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)