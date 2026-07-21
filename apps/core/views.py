# apps/core/views.py

from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .mixins import HODRequiredMixin
from .models import GalleryImage
from .forms import GalleryImageForm


class GalleryImageListView(HODRequiredMixin, ListView):
    model = GalleryImage
    template_name = 'core/gallery_list.html'
    context_object_name = 'images'
    paginate_by = 12


class GalleryImageCreateView(HODRequiredMixin, CreateView):
    model = GalleryImage
    form_class = GalleryImageForm
    template_name = 'core/gallery_form.html'
    success_url = reverse_lazy('core:gallery_list')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, "Image uploaded to gallery successfully.")
        return super().form_valid(form)


class GalleryImageDeleteView(HODRequiredMixin, DeleteView):
    model = GalleryImage
    template_name = 'core/gallery_confirm_delete.html'
    success_url = reverse_lazy('core:gallery_list')
    context_object_name = 'image'

    def form_valid(self, form):
        messages.success(self.request, "Image deleted from gallery successfully.")
        return super().form_valid(form)