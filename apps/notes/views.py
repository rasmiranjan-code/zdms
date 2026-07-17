# apps/notes/views.py

from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Note
from .forms import NoteForm
from apps.academics.models import Semester, Subject
from apps.mcqs.views import HODFacultyRequiredMixin

# --- Faculty/HOD Views ---

class NoteAuthorOrHODMixin(UserPassesTestMixin):
    def test_func(self):
        note = self.get_object()
        return self.request.user.role == 'HOD' or note.uploaded_by == self.request.user

class SelectSemesterForNotesView(HODFacultyRequiredMixin, ListView):
    model = Semester
    template_name = 'notes/select_semester.html'
    context_object_name = 'semesters'
    queryset = Semester.objects.select_related('batch__academic_session').order_by('-batch__academic_session__start_year', 'number')

class SelectSubjectForNotesView(HODFacultyRequiredMixin, ListView):
    model = Subject
    template_name = 'notes/select_subject.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        self.semester = get_object_or_404(Semester, pk=self.kwargs['semester_id'])
        return Subject.objects.filter(semester=self.semester)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['semester'] = self.semester
        return context

class NoteListView(HODFacultyRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        self.subject = get_object_or_404(Subject, pk=self.kwargs['subject_id'])
        return Note.objects.filter(subject=self.subject).select_related('uploaded_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = self.subject
        return context

class NoteUploadView(HODFacultyRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = get_object_or_404(Subject, pk=self.kwargs['subject_id'])
        return context

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        form.instance.subject_id = self.kwargs['subject_id']
        messages.success(self.request, "Note uploaded successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('notes:note_list', kwargs={'subject_id': self.kwargs['subject_id']})

class NoteUpdateView(NoteAuthorOrHODMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject'] = self.object.subject
        return context

    def get_success_url(self):
        messages.success(self.request, "Note updated successfully.")
        return reverse_lazy('notes:note_list', kwargs={'subject_id': self.object.subject.id})

class NoteDeleteView(NoteAuthorOrHODMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    context_object_name = 'note'

    def get_success_url(self):
        messages.success(self.request, "Note deleted successfully.")
        return reverse_lazy('notes:note_list', kwargs={'subject_id': self.object.subject.id})


# --- Student Views ---

class StudentSelectSemesterForNotesView(LoginRequiredMixin, ListView):
    model = Semester
    template_name = 'notes/student_select_semester.html'
    context_object_name = 'semesters'
    queryset = Semester.objects.select_related('batch__academic_session').order_by('-batch__academic_session__start_year', 'number')

class StudentSelectSubjectForNotesView(LoginRequiredMixin, ListView):
    model = Subject
    template_name = 'notes/student_select_subject.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        self.semester = get_object_or_404(Semester, pk=self.kwargs['semester_id'])
        return Subject.objects.filter(semester=self.semester)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['semester'] = self.semester
        return context

class StudentNoteListView(LoginRequiredMixin, NoteListView):
    template_name = 'notes/student_note_list.html'

class PDFViewerView(LoginRequiredMixin, View):
    def get(self, request, note_id):
        note = get_object_or_404(Note, pk=note_id)
        context = {
            'note': note,
            'pdf_url': note.file.url
        }
        return render(request, 'notes/pdf_viewer.html', context)