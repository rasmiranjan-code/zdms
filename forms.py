# apps/mcqs/forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'is_correct']
        widgets = {
            'answer_text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=4, max_num=4, can_delete=False)