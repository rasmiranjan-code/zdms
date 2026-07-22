from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    # Faculty/HOD
    path(
        "take/<int:subject_id>/<int:batch_id>/",
        views.TakeAttendanceView.as_view(),
        name="take_attendance",
    ),

    path(
        "dashboard/",
        views.AttendanceDashboardView.as_view(),
        name="attendance_dashboard",
    ),

    # Student
    path(
        "attendance/",
        views.StudentAttendanceView.as_view(),
        name="attendance",
    ),
]