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
    path('manage/<int:pk>/attempts/', views.QuizAttemptsView.as_view(), name='quiz_attempts'),
    path('manage/<int:pk>/delete/', views.QuizDeleteView.as_view(), name='delete_quiz'),

    # Student URLs
    path('', views.StudentQuizListView.as_view(), name='student_quiz_list'),
    path('start/<int:pk>/', views.StartQuizView.as_view(), name='start_quiz'),
    path('attempt/<int:pk>/', views.TakeQuizView.as_view(), name='take_quiz'),
    path('result/<int:pk>/', views.QuizResultView.as_view(), name='quiz_result'),
    path('submit/<int:pk>/', views.SubmitQuizView.as_view(), name='submit_quiz'),
]