# apps/students/urls.py

from django.urls import path
from django.views.generic import TemplateView

app_name = 'students'

urlpatterns = [
    path('dashboard/', TemplateView.as_view(template_name='students/dashboard.html'), name='dashboard'),
]