# apps/threed_library/urls.py

from django.urls import path
from . import views

app_name = 'threed_library'

urlpatterns = [
    # Faculty/HOD URLs
    path('manage/', views.ThreeDModelListView.as_view(), name='manage_list'),
    path('upload/', views.ThreeDModelUploadView.as_view(), name='upload'),
    path('edit/<int:pk>/', views.ThreeDModelUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.ThreeDModelDeleteView.as_view(), name='delete'),

    # Student URLs
    path('', views.StudentModelListView.as_view(), name='student_list'),
    path('view/<int:pk>/', views.StudentModelDetailView.as_view(), name='view_model'),
]