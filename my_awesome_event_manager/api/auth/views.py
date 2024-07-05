from dj_rest_auth.models import TokenModel
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.serializers import LoginSerializer
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from my_awesome_event_manager.api.auth.mixins import LoginMixin, LogoutMixin

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        "password",
        "old_password",
        "new_password1",
        "new_password2",
    )
)


User = get_user_model()


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class LoginView(LoginMixin):
    """
    API endpoint login.

    ---
    post:
        Check the credentials and return the REST Token
        if the credentials are valid and authenticated.
        Calls Django Auth login method to register User ID
        in Django session framework

        Accept the following POST parameters: username, password
        Return the REST Framework Token Object's key.
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel
    queryset = ""

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @extend_schema(tags=["Auth API"], operation_id="login")
    def post(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# ------------------------------------------------------------- #
# ------------------------------------------------------------- #


class LogoutView(LogoutMixin):
    """
    API endpoint logout.

    ---
    get:
        Calls Django logout method and delete the Token object
        assigned to the current User object.

        Accepts/Returns nothing.
    post:
        Calls Django logout method and delete the Token object
        assigned to the current User object.

        Accepts/Returns nothing.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.Serializer

    @extend_schema(tags=["Auth API"], operation_id="logout_get")
    def get(self, request, *args, **kwargs):
        if getattr(settings, "ACCOUNT_LOGOUT_ON_GET", False):
            response = self.logout(request)
        else:
            response = self.http_method_not_allowed(request, *args, **kwargs)
        return self.finalize_response(request, response, *args, **kwargs)

    @extend_schema(tags=["Auth API"], operation_id="logout_post")
    def post(self, request, *args, **kwargs):
        return self.logout(request)


# ------------------------------------------------------------- #
# ------------------------------------------------------------- #


class UserRegisterView(RegisterView):
    """
    Registers a new user.

    Args:
        request (HttpRequest): The HTTP request object.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        HttpResponse: The HTTP response object containing the result of the registration process.
    """

    @extend_schema(tags=["Auth API"], operation_id="signup")
    def post(self, request, *args, **kwargs):
        if User.objects.filter(email=request.data["email"]).exists():
            raise ParseError("User with this email already exists.")
        response = super().create(request, *args, **kwargs)

        if response.status_code == 204:  # User successfully created
            user = User.objects.get(email=request.data["email"])
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)

            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                "user": {
                    "user_id": user.user_id,
                    "email": user.email,
                },
                "token": token.key,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return response


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
