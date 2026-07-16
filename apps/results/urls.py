# apps/results/urls.py

from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('my-results/', views.StudentResultView.as_view(), name='my_results'),
]