# apps/quiz/forms.py

from django import forms
from .models import Quiz, QuizQuestion, Question as QuizModelQuestion, Answer as QuizAnswer
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

class ManualQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizModelQuestion
        fields = ['question_text', 'image']
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter question text here...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = QuizAnswer
        fields = ['answer_text', 'is_correct']
        widgets = {
            'answer_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter answer option...'}),
        }

AnswerFormSet = forms.inlineformset_factory(QuizModelQuestion, QuizAnswer, form=AnswerForm, extra=4, max_num=4, can_delete=False)