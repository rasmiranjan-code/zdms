# apps/quiz/views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, DetailView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import JsonResponse
import json

from .models import Quiz, QuizQuestion, StudentQuizAttempt, StudentAnswer
from .forms import QuizForm, AddQuestionToQuizForm, ManualQuestionForm, AnswerFormSet
from apps.academics.models import Semester, Subject, Enrollment
from apps.mcqs.views import HODFacultyRequiredMixin
from apps.mcqs.models import Question 

# --- Faculty/HOD Views ---

class SelectSemesterForQuizView(HODFacultyRequiredMixin, ListView):
    model = Semester
    template_name = 'quiz/select_semester.html'
    context_object_name = 'semesters'

    def get_queryset(self):
        queryset = Semester.objects.select_related('batch__academic_session').order_by('-batch__academic_session__start_year', 'number')
        batch_id = self.request.GET.get('batch')
        if batch_id:
            queryset = queryset.filter(batch_id=batch_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batches'] = Subject.objects.all().select_related('semester__batch').distinct('semester__batch')
        context['selected_batch'] = int(self.request.GET.get('batch')) if self.request.GET.get('batch') else None
        return context

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
        context['question_form'] = ManualQuestionForm()
        context['answer_formset'] = AnswerFormSet()
        context['quiz_questions'] = quiz.questions.select_related('question').all()
        return context

    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        question_form = ManualQuestionForm(request.POST, request.FILES)
        answer_formset = AnswerFormSet(request.POST)

        if question_form.is_valid() and answer_formset.is_valid():
            # Create a new question in the mcqs app
            new_question = question_form.save(commit=False)
            new_question.subject = quiz.subject
            new_question.created_by = request.user
            new_question.save()

            # Save answers for the new question
            answers = answer_formset.save(commit=False)
            for answer in answers:
                answer.question = new_question
                answer.save()

            # Link this new question to the current quiz
            quiz_question = QuizQuestion(quiz=quiz, question=new_question, marks=request.POST.get('marks', 1))
            quiz_question.quiz = quiz
            quiz_question.save()
            messages.success(request, "New question created and added to the test.")
        else:
            error_list = question_form.errors.as_text() + answer_formset.non_form_errors().as_text()
            for form in answer_formset:
                error_list += form.errors.as_text()
            messages.error(request, f"Failed to add question. Errors: {error_list}")

        return redirect('quiz:manage_quiz', pk=quiz.pk)

# --- Student Views (To be built) ---

class StudentQuizListView(LoginRequiredMixin, View):
    template_name = 'quiz/student_quiz_list.html'

    def get(self, request, *args, **kwargs):
        student = request.user
        try:
            enrollment = Enrollment.objects.get(student=student, is_active=True)
            student_subjects = Subject.objects.filter(semester=enrollment.current_semester)
            
            now = timezone.now()
            
            # Get quizzes for the student's subjects
            quizzes = Quiz.objects.filter(
                subject__in=student_subjects, 
                is_published=True
            ).order_by('-start_time')

            # Get student's attempts to mark completed quizzes
            completed_quiz_ids = StudentQuizAttempt.objects.filter(
                student=student, is_submitted=True
            ).values_list('quiz_id', flat=True)

            context = {
                'quizzes': quizzes,
                'now': now,
                'completed_quiz_ids': set(completed_quiz_ids),
            }
            return render(request, self.template_name, context)

        except Enrollment.DoesNotExist:
            messages.warning(request, "You are not enrolled in any active batch.")
            return redirect('students:dashboard')

class StartQuizView(LoginRequiredMixin, View):
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        now = timezone.now()

        # Validations
        if not (quiz.start_time <= now <= quiz.end_time):
            messages.error(request, "This test is not active right now.")
            return redirect('quiz:student_quiz_list')

        # Create or get attempt object
        attempt, created = StudentQuizAttempt.objects.get_or_create(
            student=request.user,
            quiz=quiz,
            defaults={'is_submitted': False}
        )

        if attempt.is_submitted:
            messages.info(request, "You have already submitted this test.")
            return redirect('quiz:quiz_result', pk=attempt.pk)

        return redirect('quiz:take_quiz', pk=attempt.pk)

class TakeQuizView(LoginRequiredMixin, DetailView):
    model = StudentQuizAttempt
    template_name = 'quiz/take_quiz.html'
    context_object_name = 'attempt'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempt = self.get_object()
        
        # Security check: ensure the user owns this attempt
        if attempt.student != self.request.user:
            # This should ideally not happen if URLs are correct
            raise PermissionDenied

        context['quiz_questions'] = attempt.quiz.questions.select_related('question__subject').prefetch_related('question__answers').all()
        return context

class QuizResultView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'quiz/quiz_result.html'
    context_object_name = 'quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempt'] = get_object_or_404(StudentQuizAttempt, quiz=self.get_object(), student=self.request.user)
        return context