# apps/students/urls.py

from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # HOD management of Students
    path('list/', views.StudentListView.as_view(), name='list'),

    # HOD management of Alumni Stories
    path('alumni-stories/', views.AlumniStoryListView.as_view(), name='alumni_story_list'),
    path('alumni-stories/add/', views.AlumniStoryCreateView.as_view(), name='alumni_story_add'),
    path('alumni-stories/<int:pk>/edit/', views.AlumniStoryUpdateView.as_view(), name='alumni_story_edit'),
    path(
    "dashboard/",
    views.StudentDashboardView.as_view(),
    name="dashboard",
),
    path('alumni-stories/<int:pk>/delete/', views.AlumniStoryDeleteView.as_view(), name='alumni_story_delete'),

    # Student-facing URLs
    path('profile/', views.StudentProfileView.as_view(), name='profile'),
    path('my-faculty/', views.MyFacultyView.as_view(), name='my_faculty'),
]