# apps/results/urls.py

from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('student_results/', views.MyResultsView.as_view(), name='student_results'),
]