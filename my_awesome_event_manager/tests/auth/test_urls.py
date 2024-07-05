import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


def test_signup():
    assert reverse("api:auth:rest_register") == "/api/auth/signup/"
    assert resolve("/api/auth/signup/").view_name == "api:auth:rest_register"


def test_login():
    assert reverse("api:auth:rest_login") == "/api/auth/login/"
    assert resolve("/api/auth/login/").view_name == "api:auth:rest_login"


def test_logout():
    assert reverse("api:auth:rest_logout") == "/api/auth/logout/"
    assert resolve("/api/auth/logout/").view_name == "api:auth:rest_logout"


# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
