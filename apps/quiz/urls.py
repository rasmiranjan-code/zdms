# apps/quiz/urls.py

from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    # Faculty/HOD URLs
    path('manage/', views.SelectSemesterForQuizView.as_view(), name='select_semester'),
    path('manage/semesters/<int:semester_id>/subjects/', views.SelectSubjectForQuizView.as_view(), name='select_subject'),
    path('manage/subjects/<int:subject_id>/', views.QuizListView.as_view(), name='quiz_list'),
    path('manage/subjects/<int:subject_id>/create/', views.QuizCreateView.as_view(), name='create_quiz'),
    path('manage/<int:pk>/', views.ManageQuizView.as_view(), name='manage_quiz'),
]