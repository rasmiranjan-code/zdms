# apps/core/mixins.py

from django.contrib.auth.mixins import UserPassesTestMixin

class HODRequiredMixin(UserPassesTestMixin):
    """Verify that the current user is authenticated and is an HOD."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'HOD'


class FacultyRequiredMixin(UserPassesTestMixin):
    """Verify that the current user is authenticated and is a Faculty member."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'FACULTY'


class StudentRequiredMixin(UserPassesTestMixin):
    """Verify that the current user is authenticated and is a Student."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'STUDENT'


class HODFacultyRequiredMixin(UserPassesTestMixin):
    """
    Verify that the current user is authenticated and is either an HOD or a Faculty member.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['HOD', 'FACULTY']

class HODRequiredMixin(UserPassesTestMixin):
    """Verify that the current user is authenticated and is an HOD."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'HOD'


class FacultyRequiredMixin(UserPassesTestMixin):
    """Verify that the current user is authenticated and is a Faculty member."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'FACULTY'


class StudentRequiredMixin(UserPassesTestMixin):
    """Verify that the current user is authenticated and is a Student."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'STUDENT'


class HODFacultyRequiredMixin(UserPassesTestMixin):
    """
    Verify that the current user is authenticated and is either an HOD or a Faculty member.
    """
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in ['HOD', 'FACULTY']