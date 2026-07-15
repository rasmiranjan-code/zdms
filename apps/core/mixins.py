# apps/core/mixins.py

from django.contrib.auth.mixins import UserPassesTestMixin


class HODRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and getattr(self.request.user, 'role', None) == 'HOD'


class FacultyRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and getattr(self.request.user, 'role', None) in ('FACULTY', 'HOD')


class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and getattr(self.request.user, 'role', None) == 'STUDENT'