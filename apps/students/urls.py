# apps/students/urls.py

from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('list/', views.student_list, name='list'),
    path('detail/<int:pk>/', views.student_detail, name='detail'),
    path('edit/<int:pk>/', views.StudentUpdateView.as_view(), name='edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('my-faculty/', views.my_faculty_view, name='my_faculty'),
    path('profile/', views.profile_view, name='profile'),
]