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
    path('alumni-stories/<int:pk>/delete/', views.AlumniStoryDeleteView.as_view(), name='alumni_story_delete'),
]