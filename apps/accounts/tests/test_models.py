# apps/accounts/tests/test_models.py

from django.test import TestCase
from apps.accounts.models import User


class UserModelTest(TestCase):
    def test_create_student_user(self):
        user = User.objects.create_user(username='stu1', password='pass1234', role='STUDENT')
        self.assertEqual(user.role, 'STUDENT')
        self.assertTrue(user.check_password('pass1234'))

    def test_create_faculty_user(self):
        user = User.objects.create_user(username='fac1', password='pass1234', role='FACULTY')
        self.assertEqual(user.role, 'FACULTY')