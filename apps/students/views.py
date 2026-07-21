# apps/students/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.core.mixins import HODRequiredMixin
from .models import AlumniStory
from .forms import AlumniStoryForm


class AlumniStoryListView(HODRequiredMixin, ListView):
    model = AlumniStory
    template_name = 'students/alumni_story_list.html'
    context_object_name = 'stories'
    paginate_by = 10


class AlumniStoryCreateView(HODRequiredMixin, CreateView):
    model = AlumniStory
    form_class = AlumniStoryForm
    template_name = 'students/alumni_story_form.html'
    success_url = reverse_lazy('students:alumni_story_list')

    def form_valid(self, form):
        messages.success(self.request, "Alumni story created successfully.")
        return super().form_valid(form)


class AlumniStoryUpdateView(HODRequiredMixin, UpdateView):
    model = AlumniStory
    form_class = AlumniStoryForm
    template_name = 'students/alumni_story_form.html'
    success_url = reverse_lazy('students:alumni_story_list')


class AlumniStoryDeleteView(HODRequiredMixin, DeleteView):
    model = AlumniStory
    template_name = 'students/alumni_story_confirm_delete.html'
    success_url = reverse_lazy('students:alumni_story_list')
    context_object_name = 'story'