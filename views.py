# apps/mcqs/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.core.mixins import FacultyRequiredMixin
from apps.academics.models import Semester, Subject
from .models import Question
from .forms import QuestionForm, AnswerFormSet


# --- Faculty Views ---

class FacultySelectSemesterView(FacultyRequiredMixin, ListView):
    model = Semester
    template_name = 'mcqs/faculty_select_semester.html'
    context_object_name = 'semesters'
    queryset = Semester.objects.select_related('batch__academic_session').order_by('-batch__academic_session__start_year', 'number')


class FacultySelectSubjectView(FacultyRequiredMixin, ListView):
    model = Subject
    template_name = 'mcqs/faculty_select_subject.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        self.semester = get_object_or_404(Semester, pk=self.kwargs['semester_id'])
        return Subject.objects.filter(semester=self.semester)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['semester'] = self.semester
        return context


class QuestionCreateView(FacultyRequiredMixin, View):
    template_name = 'mcqs/question_form.html'

    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        question_form = QuestionForm()
        answer_formset = AnswerFormSet()
        return render(request, self.template_name, {'subject': subject, 'question_form': question_form, 'answer_formset': answer_formset})

    @transaction.atomic
    def post(self, request, subject_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        question_form = QuestionForm(request.POST)
        answer_formset = AnswerFormSet(request.POST)

        if question_form.is_valid() and answer_formset.is_valid():
            question = question_form.save(commit=False)
            question.subject = subject
            question.created_by = request.user
            question.save()

            answers = answer_formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            
            messages.success(request, "MCQ added successfully!")
            return redirect('mcqs:add_question', subject_id=subject.id)

        return render(request, self.template_name, {'subject': subject, 'question_form': question_form, 'answer_formset': answer_formset})


# --- Student Views ---

class StudentSelectSemesterView(LoginRequiredMixin, ListView):
    model = Semester
    template_name = 'mcqs/student_select_semester.html'
    context_object_name = 'semesters'
    queryset = Semester.objects.select_related('batch__academic_session').order_by('-batch__academic_session__start_year', 'number')


class StudentSelectSubjectView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'mcqs/student_select_subject.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        self.semester = get_object_or_404(Semester, pk=self.kwargs['semester_id'])
        return Subject.objects.filter(semester=self.semester)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['semester'] = self.semester
        return context


class PracticeQuestionsView(LoginRequiredMixin, View):
    template_name = 'mcqs/practice_questions.html'

    def get(self, request, subject_id):
        subject = get_object_or_404(Subject, pk=subject_id)
        questions = Question.objects.filter(subject=subject).prefetch_related('answers', 'created_by')
        context = {
            'subject': subject,
            'questions': questions
        }
        return render(request, self.template_name, context)