# apps/accounts/views.py

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from apps.accounts.forms import LoginForm
from django.views.generic import TemplateView

class LandingPageView(TemplateView):
    template_name = 'index.html'  
class RoleBasedLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == 'STUDENT':
            return reverse_lazy('students:dashboard')
        return reverse_lazy('admin:index')