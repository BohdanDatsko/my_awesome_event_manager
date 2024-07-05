from django.urls import path

from my_awesome_event_manager.api.auth.views import (
    UserRegisterView,
    LoginView,
    LogoutView,
)

app_name = "events"

# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #

# /api/auth/...


urlpatterns = [
    # URLs that do not require a session or valid token
    path("signup/", UserRegisterView.as_view(), name="rest_register"),
    path("login/", LoginView.as_view({"post": "post"}), name="rest_login"),
    # URLs that require a user to be logged in with a valid session / token.
    path(
        "logout/",
        LogoutView.as_view({"get": "get", "post": "post"}),
        name="rest_logout",
    ),
]


# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
