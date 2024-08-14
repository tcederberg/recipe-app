from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.login_url = reverse(
            "login"
        )  # Update with the correct name of your login URL
        self.logout_url = reverse(
            "logout_success"
        )  # Update with the correct name of your logout URL

    def test_login_view(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "12345"}
        )
        self.assertEqual(
            response.status_code, 302
        )  # Assuming redirect after successful login
        self.assertTrue(
            "_auth_user_id" in self.client.session
        )  # Check if the user is logged in




class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="Jim", password="password123")

    def test_user_name(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("username").verbose_name
        self.assertEqual(field_label, "username")

    def test_username_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("username").max_length
        self.assertEqual(max_length, 150)  # Default max_length for username
