# apps/accounts/tests/test_permissions.py

from django.test import TestCase
from apps.accounts.models import User
from apps.accounts.permissions import is_hod, is_faculty, is_student


class PermissionHelperTest(TestCase):
    def setUp(self):
        self.hod = User.objects.create_user(username='hod1', password='pass1234', role='HOD')
        self.faculty = User.objects.create_user(username='fac1', password='pass1234', role='FACULTY')
        self.student = User.objects.create_user(username='stu1', password='pass1234', role='STUDENT')

    def test_is_hod(self):
        self.assertTrue(is_hod(self.hod))
        self.assertFalse(is_hod(self.faculty))

    def test_is_faculty(self):
        self.assertTrue(is_faculty(self.faculty))
        self.assertTrue(is_faculty(self.hod))
        self.assertFalse(is_faculty(self.student))

    def test_is_student(self):
        self.assertTrue(is_student(self.student))
        self.assertFalse(is_student(self.faculty))