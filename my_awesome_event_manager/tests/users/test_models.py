from django.test import TestCase

from my_awesome_event_manager.events.models import User
from my_awesome_event_manager.tests.users.factories import UserFactory


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class UserTests(TestCase):
    @staticmethod
    def create_user() -> User:
        return UserFactory()

    def test_create_user(self):
        user = self.create_user()

        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), f"{user.email}")

    def test_update_user(self):
        user = self.create_user()
        user.first_name = "John"
        user.last_name = "Doe"
        user.save()

        self.assertEqual(User.objects.filter(first_name="John", last_name="Doe").count(), 1)

    def test_remove_user(self):
        user = self.create_user()
        user.delete()

        self.assertEqual(User.objects.count(), 0)


    def test_user_get_absolute_url(self):
        user = self.create_user()
        assert user.get_absolute_url() == f"/api/users/{user.user_id}/"


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
