# apps/faculty_attendance/urls.py

from django.urls import path
from . import views

app_name = 'faculty_attendance'

urlpatterns = [
    path('', views.TakeFacultyAttendanceView.as_view(), name='take_attendance'),
]