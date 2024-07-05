from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser

from my_awesome_event_manager.api.users.mixins import UserMixin, UserUUIDMixin
from my_awesome_event_manager.api.users.permissions import IsRequestUserOrAdmin
from my_awesome_event_manager.api.users.serializers import UserCompactSerializer, UserSerializer, UserUUIDSerializer

User = get_user_model()


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class UserListView(UserMixin):
    """
    API endpoint get multiple users.

    ---
    get:
        Get multiple users.

        Returns the user records for all users in all workspaces accessible to the authenticated user.
        Accepts an optional workspace ID parameter. Results are sorted by user ID.
    """

    model = User
    queryset = User.objects.all()
    serializer_class = UserCompactSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return super().get_queryset().only("user_id", "email")

    @extend_schema(tags=["Users API"], operation_id="users_list")
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


# ------------------------------------------------------------- #
# ------------------------------------------------------------- #


class UserGetUpdateView(UserMixin):
    """
    API endpoint User details.

    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.

    Default accepted fields: username, first_name, last_name
    Default display fields: pk, username, email, first_name, last_name
    Read-only fields: pk, email

    ---
    get:
        Get a user.

        Returns the full user record for the single user with the provided ID. Results are sorted by user ID.
    put:
        Update a user.

        Returns the full updated user record for the single user with the provided ID.
    """

    model = User
    lookup_field = "user_id"
    lookup_url_kwarg = "user_id"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsRequestUserOrAdmin,)

    @extend_schema(tags=["Users API"], operation_id="user_by_id_retrieve")
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(tags=["Users API"], operation_id="user_by_id_update")
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


# ------------------------------------------------------------- #
# ------------------------------------------------------------- #


class UserUUIDView(UserUUIDMixin):
    """
    API endpoint get user's UUID.

    ---
    get:
        Get user's UUID.

        Returns the user's UUID.
    """

    model = User
    queryset = User.objects.all()
    serializer_class = UserUUIDSerializer

    def get_object(self):
        """
        Returns the currently authenticated user.
        """
        return self.request.user

    @extend_schema(tags=["Users API"], operation_id="get_user_uuid")
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
