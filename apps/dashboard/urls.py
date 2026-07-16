# apps/dashboard/urls.py

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('hod/', views.HODDashboardView.as_view(), name='hod_dashboard'),
    path('faculty/', views.FacultyDashboardView.as_view(), name='faculty_dashboard'),
]