# apps/results/views.py

from django.views.generic import TemplateView
from apps.core.mixins import StudentRequiredMixin

class MyResultsView(StudentRequiredMixin, TemplateView):
    template_name = 'results/student_results.html'