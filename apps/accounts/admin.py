# apps/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.accounts.models import User, FacultySubjectBatchMapping, ClassCoordinatorAssignment


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'role', 'email', 'is_active', 'created_by')
    list_filter = ('role', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role', 'phone_number', 'created_by')}),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(FacultySubjectBatchMapping)
class FacultySubjectBatchMappingAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'subject', 'batch')
    list_filter = ('batch', 'subject')


@admin.register(ClassCoordinatorAssignment)
class ClassCoordinatorAssignmentAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'batch')