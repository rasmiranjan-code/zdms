# apps/results/views.py

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Result
from collections import defaultdict


class StudentResultView(LoginRequiredMixin, View):
    template_name = 'results/student_results.html'

    def get(self, request, *args, **kwargs):
        student = request.user
        results_by_semester = defaultdict(list)
        
        results = Result.objects.filter(student=student).select_related('subject', 'semester__batch__academic_session')
        
        for result in results:
            results_by_semester[result.semester].append(result)

        context = {'results_by_semester': dict(results_by_semester)}
        return render(request, self.template_name, context)