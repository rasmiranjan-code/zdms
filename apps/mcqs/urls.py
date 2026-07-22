# apps/mcqs/urls.py

from django.urls import path
from . import views

app_name = 'mcqs'

urlpatterns = [
    # Faculty URLs
    path('faculty/semesters/', views.FacultySelectSemesterView.as_view(), name='faculty_select_semester'),
    path('faculty/semesters/<int:semester_id>/subjects/', views.FacultySelectSubjectView.as_view(), name='faculty_select_subject'),    
    path('faculty/subjects/<int:subject_id>/', views.QuestionListView.as_view(), name='question_list'),
    path('faculty/subjects/<int:subject_id>/add/', views.QuestionCreateView.as_view(), name='add_question'),
    path('faculty/questions/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='edit_question'),
    path('faculty/questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='delete_question'),

    # HOD URLs
    path('hod/semesters/', views.FacultySelectSemesterView.as_view(), name='hod_select_semester'),
    path('hod/semesters/<int:semester_id>/subjects/', views.FacultySelectSubjectView.as_view(), name='hod_select_subject'),
    path('hod/subjects/<int:subject_id>/', views.QuestionListView.as_view(), name='hod_question_list'),

    # Reports / Analytics
    path('reports/student-accuracy/', views.StudentAccuracyReportView.as_view(), name='student_accuracy_report'),
    path('reports/student-history/<int:student_id>/', views.StudentAttemptHistoryView.as_view(), name='student_attempt_history'),

    # Student URLs
    path('practice/', views.StudentSelectSemesterView.as_view(), name='student_select_semester'),
    path('practice/semesters/<int:semester_id>/subjects/', views.StudentSelectSubjectView.as_view(), name='student_select_subject'),
    path('practice/subjects/<int:subject_id>/', views.PracticeQuestionsView.as_view(), name='practice_questions'),
    path('practice/subjects/<int:subject_id>/submit/', views.SubmitPracticeView.as_view(), name='submit_practice'),
    path('practice/log-attempt/', views.log_student_attempt, name='log_attempt'),
]
