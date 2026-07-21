# d:/zdms/apps/students/admin.py
from django.contrib import admin
from .models import StudentProfile, AlumniStory

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'college_roll_number', 'university_roll_number')

@admin.register(AlumniStory)
class AlumniStoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'current_role', 'is_featured')
    list_filter = ('is_featured',)
    search_fields = ('student__first_name', 'student__last_name', 'current_role')
