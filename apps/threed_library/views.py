# apps/threed_library/views.py

from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.core.mixins import StudentRequiredMixin, HODFacultyRequiredMixin
from .models import ThreeDModel
from .forms import ThreeDModelForm


# --- HOD/Faculty Management Views ---

class ThreeDModelListView(HODFacultyRequiredMixin, ListView):
    model = ThreeDModel
    template_name = 'threed_library/manage_list.html'
    context_object_name = 'models'

class ThreeDModelUploadView(HODFacultyRequiredMixin, CreateView):
    model = ThreeDModel
    form_class = ThreeDModelForm
    template_name = 'threed_library/model_form.html'
    success_url = reverse_lazy('threed_library:manage_list')

class ThreeDModelUpdateView(HODFacultyRequiredMixin, UpdateView):
    model = ThreeDModel
    form_class = ThreeDModelForm
    template_name = 'threed_library/model_form.html'
    success_url = reverse_lazy('threed_library:manage_list')

class ThreeDModelDeleteView(HODFacultyRequiredMixin, DeleteView):
    model = ThreeDModel
    template_name = 'threed_library/model_confirm_delete.html'
    success_url = reverse_lazy('threed_library:manage_list')

# --- Student-facing Views ---

class StudentModelListView(StudentRequiredMixin, TemplateView):
    template_name = 'threed_library/student_list.html'

class StudentModelDetailView(LoginRequiredMixin, DetailView):
    model = ThreeDModel
    template_name = 'threed_library/student_model_detail.html'
    context_object_name = 'model'