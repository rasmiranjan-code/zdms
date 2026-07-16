# apps/mcqs/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from apps.core.mixins import FacultyRequiredMixin
from apps.academics.models import Semester, Subject, Batch, Enrollment
from apps.accounts.models import User
from .models import Question, QuestionEditHistory, StudentAttempt, Answer
from .forms import QuestionForm, AnswerFormSet
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json


class HODFacultyRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['HOD', 'FACULTY']



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

class QuestionListView(FacultyRequiredMixin, ListView):
    model = Question
    template_name = 'mcqs/question_list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        self.subject = get_object_or_404(Subject, pk=self.kwargs['subject_id'])
        return Question.objects.filter(subject=self.subject).select_related('created_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = self.subject
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
        question_form = QuestionForm(request.POST, request.FILES)
        answer_formset = AnswerFormSet(request.POST, request.FILES)

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
            return redirect('mcqs:question_list', subject_id=subject.id)

        return render(request, self.template_name, {'subject': subject, 'question_form': question_form, 'answer_formset': answer_formset})

class QuestionUpdateView(FacultyRequiredMixin, View):
    template_name = 'mcqs/question_form.html'

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        question_form = QuestionForm(instance=question)
        answer_formset = AnswerFormSet(instance=question)
        context = {
            'subject': question.subject,
            'question_form': question_form,
            'answer_formset': answer_formset,
            'question': question, # For history
        }
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        question_form = QuestionForm(request.POST, request.FILES, instance=question)
        answer_formset = AnswerFormSet(request.POST, request.FILES, instance=question)

        if question_form.is_valid() and answer_formset.is_valid():
            question_form.save()
            answer_formset.save()
            
            # Log the edit history
            QuestionEditHistory.objects.create(question=question, edited_by=request.user)

            messages.success(request, "MCQ updated successfully!")
            return redirect('mcqs:question_list', subject_id=question.subject.id)

        context = {
            'subject': question.subject,
            'question_form': question_form,
            'answer_formset': answer_formset,
            'question': question,
        }
        return render(request, self.template_name, context)

class QuestionDeleteView(FacultyRequiredMixin, DeleteView):
    model = Question
    template_name = 'mcqs/question_confirm_delete.html'
    context_object_name = 'question'

    def get_success_url(self):
        messages.success(self.request, "Question deleted successfully.")
        # Check user role to redirect to the correct list
        if self.request.user.role == 'HOD':
            return reverse_lazy('mcqs:hod_question_list', kwargs={'subject_id': self.object.subject.id})
        return reverse_lazy('mcqs:question_list', kwargs={'subject_id': self.object.subject.id})


# --- Analytics/Reports ---

class StudentAccuracyReportView(HODFacultyRequiredMixin, View):
    template_name = 'mcqs/student_accuracy_report.html'

    def get(self, request, *args, **kwargs):
        batch_id = request.GET.get('batch')
        
        # Base queryset
        attempts = StudentAttempt.objects.all()

        if batch_id:
            # Get student IDs for the selected batch
            student_ids = Enrollment.objects.filter(batch_id=batch_id).values_list('student_id', flat=True)
            attempts = attempts.filter(student_id__in=student_ids)

        # Aggregate accuracy per student per subject
        student_accuracy_data = attempts.values(
            'student__id', 'student__first_name', 'student__last_name',
            'question__subject__name', 'question__subject__semester__number'
        ).annotate(
            total_attempts=Count('id'),
            correct_attempts=Count('id', filter=Q(is_correct=True))
        ).order_by('student__last_name', 'student__first_name', 'question__subject__semester__number')

        # Process data for template
        report = {}
        for item in student_accuracy_data:
            student_id = item['student__id']
            if student_id not in report:
                report[student_id] = {'name': f"{item['student__first_name']} {item['student__last_name']}", 'subjects': []}
            
            accuracy = (item['correct_attempts'] / item['total_attempts'] * 100) if item['total_attempts'] > 0 else 0
            report[student_id]['subjects'].append({'name': item['question__subject__name'], 'accuracy': accuracy, 'attempts': item['total_attempts']})

        context = {'report': report, 'batches': Batch.objects.all(), 'selected_batch': int(batch_id) if batch_id else None}
        return render(request, self.template_name, context)


class StudentAttemptHistoryView(HODFacultyRequiredMixin, View):
    template_name = 'mcqs/student_attempt_history.html'

    def get(self, request, student_id):
        student = get_object_or_404(User, pk=student_id)
        attempts = StudentAttempt.objects.filter(student=student).select_related(
            'question__subject', 'selected_answer'
        ).order_by('-created_at')

        context = {
            'student': student,
            'attempts': attempts
        }
        return render(request, self.template_name, context)
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

@login_required
def log_student_attempt(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question_id = data.get('question_id')
        answer_id = data.get('answer_id')

        try:
            question = Question.objects.get(pk=question_id)
            selected_answer = Answer.objects.get(pk=answer_id)
            
            StudentAttempt.objects.create(
                student=request.user,
                question=question,
                selected_answer=selected_answer,
                is_correct=selected_answer.is_correct
            )
            return JsonResponse({'status': 'success'})
        except (Question.DoesNotExist, Answer.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)