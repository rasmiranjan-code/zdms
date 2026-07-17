# apps/notes/urls.py

from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    # Faculty/HOD URLs
    path('manage/', views.SelectSemesterForNotesView.as_view(), name='select_semester'),
    path('manage/semesters/<int:semester_id>/subjects/', views.SelectSubjectForNotesView.as_view(), name='select_subject'),
    path('manage/subjects/<int:subject_id>/', views.NoteListView.as_view(), name='note_list'),
    path('manage/subjects/<int:subject_id>/upload/', views.NoteUploadView.as_view(), name='upload_note'),
    path('manage/note/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='edit_note'),
    path('manage/note/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='delete_note'),
    # Student URLs
    path('', views.StudentSelectSemesterForNotesView.as_view(), name='student_select_semester'),
    path('semesters/<int:semester_id>/subjects/', views.StudentSelectSubjectForNotesView.as_view(), name='student_select_subject'),
    path('subjects/<int:subject_id>/', views.StudentNoteListView.as_view(), name='student_note_list'),
    path('view/<int:note_id>/', views.PDFViewerView.as_view(), name='view_note'),
]