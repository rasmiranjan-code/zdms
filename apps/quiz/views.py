# apps/quiz/views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Quiz, QuizQuestion
from .forms import QuizForm, AddQuestionToQuizForm
from apps.academics.models import Semester, Subject
from apps.mcqs.views import HODFacultyRequiredMixin
from apps.mcqs.models import Question

# --- Faculty/HOD Views ---

class SelectSemesterForQuizView(HODFacultyRequiredMixin, ListView):
    model = Semester
    template_name = 'quiz/select_semester.html'
    context_object_name = 'semesters'
    queryset = Semester.objects.select_related('batch__academic_session').order_by('-batch__academic_session__start_year', 'number')

class SelectSubjectForQuizView(HODFacultyRequiredMixin, ListView):
    model = Subject
    template_name = 'quiz/select_subject.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        self.semester = get_object_or_404(Semester, pk=self.kwargs['semester_id'])
        return Subject.objects.filter(semester=self.semester)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['semester'] = self.semester
        return context

class QuizListView(HODFacultyRequiredMixin, ListView):
    model = Quiz
    template_name = 'quiz/quiz_list.html'
    context_object_name = 'quizzes'

    def get_queryset(self):
        self.subject = get_object_or_404(Subject, pk=self.kwargs['subject_id'])
        return Quiz.objects.filter(subject=self.subject)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = self.subject
        return context

class QuizCreateView(HODFacultyRequiredMixin, CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quiz/quiz_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['subject_id'])
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.subject_id = self.kwargs['subject_id']
        messages.success(self.request, "Test created successfully. Now add questions.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('quiz:manage_quiz', kwargs={'pk': self.object.pk})

class ManageQuizView(HODFacultyRequiredMixin, DetailView):
    model = Quiz
    template_name = 'quiz/manage_quiz.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()
        form = AddQuestionToQuizForm()
        # Only show questions from the same subject that are not already in the quiz
        existing_question_ids = quiz.questions.values_list('question_id', flat=True)
        form.fields['question'].queryset = Question.objects.filter(
            subject=quiz.subject
        ).exclude(id__in=existing_question_ids)
        context['form'] = form
        context['quiz_questions'] = quiz.questions.select_related('question').all()
        return context

    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        form = AddQuestionToQuizForm(request.POST)
        form.fields['question'].queryset = Question.objects.filter(subject=quiz.subject) # Re-set queryset for validation

        if form.is_valid():
            quiz_question = form.save(commit=False)
            quiz_question.quiz = quiz
            quiz_question.save()
            messages.success(request, "Question added to the test.")
        else:
            messages.error(request, "Failed to add question. Please check the form.")

        return redirect('quiz:manage_quiz', pk=quiz.pk)

# --- Student Views (To be built) ---

class StudentQuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'quiz/student_quiz_list.html'
    context_object_name = 'quizzes'

    def get_queryset(self):
        # This needs to be more complex, finding quizzes for the student's batch/semester
        return Quiz.objects.filter(is_published=True).order_by('-start_time')