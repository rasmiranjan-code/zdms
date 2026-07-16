# apps/mcqs/urls.py

from django.urls import path
from . import views

app_name = 'mcqs'

urlpatterns = [
    # Faculty URLs
    path('faculty/semesters/', views.FacultySelectSemesterView.as_view(), name='faculty_select_semester'),
    path('faculty/semesters/<int:semester_id>/subjects/', views.FacultySelectSubjectView.as_view(), name='faculty_select_subject'),
    path('faculty/subjects/<int:subject_id>/add/', views.QuestionCreateView.as_view(), name='add_question'),
    # Student URLs
    path('practice/', views.StudentSelectSemesterView.as_view(), name='student_select_semester'),
    path('practice/semesters/<int:semester_id>/subjects/', views.StudentSelectSubjectView.as_view(), name='student_select_subject'),
    path('practice/subjects/<int:subject_id>/', views.PracticeQuestionsView.as_view(), name='practice_questions'),
]