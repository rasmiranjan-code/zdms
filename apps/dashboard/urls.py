# apps/dashboard/urls.py

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('hod/', views.TemplateView.as_view(template_name='registration/hod_dashboard.html'), name='hod_dashboard'),
    path('faculty/', views.FacultyDashboardView.as_view(), name='faculty_dashboard'),
]