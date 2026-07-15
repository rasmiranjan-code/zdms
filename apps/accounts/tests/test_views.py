# apps/accounts/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import User


class LoginViewTest(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='stu1', password='pass1234', role='STUDENT')

    def test_login_page_loads(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_student_login_redirect(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'stu1', 'password': 'pass1234'
        })
        self.assertEqual(response.status_code, 302)