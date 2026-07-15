# apps/students/urls.py

from django.urls import path
from . import views 

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('my-faculty/', views.my_faculty_view, name='my_faculty'),
    path('<int:pk>/edit/', views.StudentUpdateView.as_view(), name='edit'),
    path('<int:pk>/', views.student_detail, name='detail'),
    path('', views.student_list, name='list'),
]