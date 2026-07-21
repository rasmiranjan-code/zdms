# d:/zdms/apps/students/admin.py
from django.contrib import admin
from .models import StudentProfile, AlumniStory

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'college_roll_number', 'university_roll_number')

@admin.register(AlumniStory)
class AlumniStoryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'batch_year', 'current_role', 'is_featured')
    list_filter = ('is_featured', 'batch_year')
    search_fields = ('student_name', 'current_role')
