from django.urls import path

from my_awesome_event_manager.api.users.views import UserListView, UserGetUpdateView

app_name = "users"

# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #

# /api/users/...

urlpatterns = [
    path("", UserListView.as_view({"get": "get"}), name="users"),
    path(
        "<uuid:user_id>/",
        UserGetUpdateView.as_view({"get": "get", "put": "put"}),
        name="user_by_id",
    ),
]

# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
