# apps/academics/urls.py

from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('sessions/', views.AcademicSessionListView.as_view(), name='session_list'),
    path('sessions/add/', views.AcademicSessionCreateView.as_view(), name='session_add'),
    path('batches/', views.BatchListView.as_view(), name='batch_list'),
    path('batches/add/', views.BatchCreateView.as_view(), name='batch_add'),
    path('semesters/', views.SemesterListView.as_view(), name='semester_list'),
    path('semesters/add/', views.SemesterCreateView.as_view(), name='semester_add'),
    path('ajax/get-semesters/', views.get_semesters_for_batch, name='ajax_get_semesters'),
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/add/', views.SubjectCreateView.as_view(), name='subject_add'),
]