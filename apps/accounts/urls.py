# apps/accounts/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from apps.accounts.views import (
    RoleBasedLoginView, LandingPageView, HODCreateStudentView, FacultyAssignmentListView, 
    FacultyAssignView, HODCreateFacultyView, HODSettingsView, FacultyDetailView, 
    FacultyUpdateView, FacultyPasswordChangeView
)

app_name = 'accounts'

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('hod/students/add/', HODCreateStudentView.as_view(), name='hod_add_student'),
    path('hod/faculty/add/', HODCreateFacultyView.as_view(), name='hod_add_faculty'),
    path('hod/settings/', HODSettingsView.as_view(), name='hod_settings'),
    path('faculty/assignments/', FacultyAssignmentListView.as_view(), name='faculty_assignment_list'),
    path('faculty/assign/', FacultyAssignView.as_view(), name='faculty_assign'),
    path('faculty/<int:pk>/', FacultyDetailView.as_view(), name='faculty_detail'),
    path('faculty/<int:pk>/edit/', FacultyUpdateView.as_view(), name='faculty_edit'),
    path('faculty/<int:pk>/change-password/', FacultyPasswordChangeView.as_view(), name='faculty_change_password'),
    path('login/', RoleBasedLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:landing'), name='logout'),
]