# zdms_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('students/', include('apps.students.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('academics/', include('apps.academics.urls')),
    path('attendance/', include('apps.attendance.urls')),
    path('mcqs/', include('apps.mcqs.urls')),
    path('results/', include('apps.results.urls')),
    path('notices/', include('apps.notices.urls')),
    path('notes/', include('apps.notes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)