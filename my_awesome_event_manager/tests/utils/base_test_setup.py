from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from my_awesome_event_manager.tests.users.factories import UserFactory
from my_awesome_event_manager.tests.utils.factories import TokenFactory


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.token = TokenFactory(user=self.user).key
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {self.token}"}
        self.fake_auth_headers = {"HTTP_AUTHORIZATION": "Token NOT REAL"}

    def get_objects(self):
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.json().get("results"), [])

    def get_objects_not_found(self):
        response = self.client.get(self.url_not_found, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def create_objects(self):
        response = self.client.post(
            self.url,
            self.body,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def create_objects_bad_request(self):
        response = self.client.post(self.url, format="json", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def create_objects_denied(self):
        response = self.client.post(
            self.url_denied,
            self.body,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json().get("error").get("message"),
            "You do not have permissions for this API endpoint",
        )

    def get_object_by_id(self):
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_object_by_id_not_found(self):
        response = self.client.get(self.url_not_found, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def update_object_by_id(self):
        response = self.client.put(
            self.url,
            self.body,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def update_object_without_body_by_id(self):
        response = self.client.put(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def update_object_by_id_bad_request(self):
        response = self.client.put(self.url, self.body, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def update_object_by_id_not_found(self):
        response = self.client.put(
            self.url_not_found,
            self.body,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def update_object_by_id_forbidden(self):
        response = self.client.put(
            self.url_forbidden,
            self.body,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def delete_object_by_id(self):
        response = self.client.delete(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_object_by_id_not_found(self):
        response = self.client.delete(self.url_not_found, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def delete_object_by_id_forbidden(self):
        response = self.client.delete(self.url_forbidden, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def add_object(self):
        response = self.client.post(
            self.url_add,
            self.body,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def add_object_forbidden(self):
        response = self.client.post(
            self.url_add_forbidden,
            self.body,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def add_object_bad_request(self):
        response = self.client.post(self.url_add, self.body, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def remove_object(self):
        response = self.client.post(
            self.url_remove,
            self.body,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def remove_object_forbidden(self):
        response = self.client.post(
            self.url_remove_forbidden,
            self.body,
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def remove_object_bad_request(self):
        response = self.client.post(self.url_remove, self.body, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
