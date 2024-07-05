import pytest
from django.urls import resolve, reverse

from my_awesome_event_manager.events.models import User

pytestmark = pytest.mark.django_db


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


def test_list_users():
    assert reverse("api:users:users") == "/api/users/"
    assert resolve("/api/users/").view_name == "api:users:users"


def test_detail(user: User):
    assert reverse("api:users:user_by_id", kwargs={"user_id": user.user_id}) == f"/api/users/{user.user_id}/"
    assert resolve(f"/api/users/{user.user_id}/").view_name == "api:users:user_by_id"


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
