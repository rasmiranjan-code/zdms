# apps/attendance/urls.py

from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('take/<int:subject_id>/<int:batch_id>/', views.TakeAttendanceView.as_view(), name='take_attendance'),
]