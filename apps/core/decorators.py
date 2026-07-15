# apps/core/decorators.py

from functools import wraps
from django.core.exceptions import PermissionDenied


def hod_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, 'role', None) != 'HOD':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped


def faculty_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, 'role', None) not in ('FACULTY', 'HOD'):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped


def student_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, 'role', None) != 'STUDENT':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped