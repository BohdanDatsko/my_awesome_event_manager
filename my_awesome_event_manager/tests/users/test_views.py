from django.urls import reverse
from rest_framework import status

from my_awesome_event_manager.tests.utils.base_test_setup import BaseAPITestCase


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class UserListTest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("api:users:users")

    def test_list_users(self):
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_by_admin(self):
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class UserGetUpdateTest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.body = {
            "first_name": "John",
            "last_name": "Doe",
        }
        self.url = reverse("api:users:user_by_id", kwargs={"user_id": self.user.user_id})

    def test_get_user_by_id_by_admin(self):
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_by_id_by_admin(self):
        self.user.is_staff = True
        self.user.save()
        response = self.client.put(
            self.url,
            self.body,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_by_id(self):
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_by_id(self):
        response = self.client.put(
            self.url,
            self.body,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_by_id_forbidden(self):
        response = self.client.get(self.url, **self.fake_auth_headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_by_id_forbidden(self):
        response = self.client.put(
            self.url,
            self.body,
            format="json",
            **self.fake_auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
