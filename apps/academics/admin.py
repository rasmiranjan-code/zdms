# apps/academics/admin.py

from django.contrib import admin
from apps.academics.models import AcademicSession, Batch, Semester, Subject, Enrollment

admin.site.register(AcademicSession)
admin.site.register(Batch)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Enrollment)