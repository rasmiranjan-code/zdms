from django.urls import path
from .views import TakeFacultyAttendanceView

app_name = "faculty_attendance"

urlpatterns = [
    path(
        "take/",
        TakeFacultyAttendanceView.as_view(),
        name="take_attendance",
    ),
]