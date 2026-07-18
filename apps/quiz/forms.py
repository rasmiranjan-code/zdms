# apps/quiz/forms.py

from django import forms
from .models import Quiz, QuizQuestion
from apps.mcqs.models import Question

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'duration_minutes', 'start_time', 'end_time', 'total_marks', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AddQuestionToQuizForm(forms.ModelForm):
    question = forms.ModelChoiceField(
        queryset=Question.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = QuizQuestion
        fields = ['question', 'marks']
        widgets = {
            'marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }