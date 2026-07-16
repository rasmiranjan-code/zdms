from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Notice
from .forms import NoticeForm
from apps.mcqs.views import HODFacultyRequiredMixin # Reusing the mixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class NoticeAuthorOrHODMixin(UserPassesTestMixin):
    """Mixin to allow access only to the notice author or an HOD."""
    def test_func(self):
        notice = self.get_object()
        return self.request.user.role == 'HOD' or notice.posted_by == self.request.user

class NoticeUploadView(HODFacultyRequiredMixin, CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'notices/notice_form.html'
    success_url = reverse_lazy('notices:upload_notice')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        messages.success(self.request, "Notice uploaded successfully.")
        return super().form_valid(form)

class NoticeListView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = 'notices/notice_list.html'
    context_object_name = 'notices'
    paginate_by = 10

class NoticeUpdateView(NoticeAuthorOrHODMixin, UpdateView):
    model = Notice
    form_class = NoticeForm
    template_name = 'notices/notice_form.html'

    def get_success_url(self):
        messages.success(self.request, "Notice updated successfully.")
        return reverse_lazy('notices:notice_list')

class NoticeDeleteView(NoticeAuthorOrHODMixin, DeleteView):
    model = Notice
    template_name = 'notices/notice_confirm_delete.html'
    context_object_name = 'notice'
    success_url = reverse_lazy('notices:notice_list')

    def form_valid(self, form):
        messages.success(self.request, "Notice deleted successfully.")
        return super().form_valid(form)
