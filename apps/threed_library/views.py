# apps/threed_library/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from .models import ThreeDModel
from .forms import ThreeDModelForm
from apps.mcqs.views import HODFacultyRequiredMixin

class ModelAuthorOrHODMixin(UserPassesTestMixin):
    """Mixin to allow access only to the model author or an HOD."""
    def test_func(self):
        model = self.get_object()
        return self.request.user.role == 'HOD' or model.uploaded_by == self.request.user

class ThreeDModelListView(HODFacultyRequiredMixin, ListView):
    model = ThreeDModel
    template_name = 'threed_library/model_list.html'
    context_object_name = 'models'
    paginate_by = 12

class ThreeDModelUploadView(HODFacultyRequiredMixin, CreateView):
    model = ThreeDModel
    form_class = ThreeDModelForm
    template_name = 'threed_library/model_form.html'
    success_url = reverse_lazy('threed_library:manage_list')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, "3D Model uploaded successfully.")
        return super().form_valid(form)

class ThreeDModelUpdateView(ModelAuthorOrHODMixin, UpdateView):
    model = ThreeDModel
    form_class = ThreeDModelForm
    template_name = 'threed_library/model_form.html'
    success_url = reverse_lazy('threed_library:manage_list')

class ThreeDModelDeleteView(ModelAuthorOrHODMixin, DeleteView):
    model = ThreeDModel
    template_name = 'threed_library/model_confirm_delete.html'
    context_object_name = 'model'
    success_url = reverse_lazy('threed_library:manage_list')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, f"Model '{self.get_object().title}' has been deleted.")
        return super().post(request, *args, **kwargs)


# --- Student Views ---

class StudentModelListView(LoginRequiredMixin, ListView):
    model = ThreeDModel
    template_name = 'threed_library/student_model_list.html'
    context_object_name = 'models'
    paginate_by = 12

class StudentModelDetailView(LoginRequiredMixin, DetailView):
    model = ThreeDModel
    template_name = 'threed_library/student_model_detail.html'
    context_object_name = 'model'
