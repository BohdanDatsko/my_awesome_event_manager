from django.urls import reverse
from rest_framework import status

from my_awesome_event_manager.tests.users.factories import UserFactory
from my_awesome_event_manager.tests.utils.base_test_setup import BaseAPITestCase


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class RegisterViewTest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("api:auth:rest_register")

    def test_successful_registration(self):
        data = {
            "email": "test@example.com",
            "password1": "test_password",
            "password2": "test_password",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_with_mismatched_passwords(self):
        data = {
            "email": "test@example.com",
            "password1": "test_password",
            "password2": "different_password",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_existing_email(self):
        UserFactory(email="test@example.com")
        data = {
            "email": "test@example.com",
            "password1": "test_password",
            "password2": "test_password",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class LoginViewTest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory(
            email="johndoe@email.com", password="my_very_safe_password"
        )
        self.url = reverse("api:auth:rest_login")

    def test_successful_login(self):
        data = {
            "email": "johndoe@email.com",
            "password": "my_very_safe_password",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_email(self):
        data = {
            "email": "johndoe@email.com",
            "password": "my_unsafe_password",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class LogoutViewTest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("api:auth:rest_logout")

    def test_successful_logout(self):
        response = self.client.post(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_method_not_allowed(self):
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
