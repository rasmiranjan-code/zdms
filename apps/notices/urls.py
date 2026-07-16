from django.urls import path
from . import views

app_name = 'notices'

urlpatterns = [
    path('upload/', views.NoticeUploadView.as_view(), name='upload_notice'),
    path('view/', views.NoticeListView.as_view(), name='notice_list'),
    path('<int:pk>/edit/', views.NoticeUpdateView.as_view(), name='edit_notice'),
    path('<int:pk>/delete/', views.NoticeDeleteView.as_view(), name='delete_notice'),
]
