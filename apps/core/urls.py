# apps/core/urls.py

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('gallery/', views.GalleryImageListView.as_view(), name='gallery_list'),
    path('gallery/upload/', views.GalleryImageCreateView.as_view(), name='gallery_upload'),
    path('gallery/<int:pk>/delete/', views.GalleryImageDeleteView.as_view(), name='gallery_delete'),
]