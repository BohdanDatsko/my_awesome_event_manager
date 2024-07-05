from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.models import get_token_model
from dj_rest_auth.serializers import TokenSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

from my_awesome_event_manager.api.mixins import BaseMixin
from my_awesome_event_manager.core.decorators import calculate_api_time

User = get_user_model()


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class LoginMixin(BaseMixin):
    def __init__(self):
        super().__init__()
        self.user = None
        self.token = None
        self.serializer = None

    def process_login(self):
        django_login(self.request, self.user)

    @staticmethod
    def get_response_serializer():
        response_serializer = TokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data["user"]
        token_model = get_token_model()
        self.token = api_settings.TOKEN_CREATOR(token_model, self.user, self.serializer)
        if getattr(settings, "REST_SESSION_LOGIN", True):
            self.process_login()

    @calculate_api_time
    def retrieve(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data, context={"request": request})
        self.serializer.is_valid(raise_exception=True)
        self.login()

        serializer_class = self.get_response_serializer()
        serializer = serializer_class(instance=self.token, context={"request": self.request})
        return Response(
            self.get_results(
                results_count=1,
                results={
                    **serializer.data,
                    "user_id": self.user.user_id,
                },
            ),
            status=status.HTTP_200_OK,
        )


# ------------------------------------------------------------- #
# ------------------------------------------------------------- #


class LogoutMixin(BaseMixin):
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, "REST_SESSION_LOGIN", True):
            django_logout(request)

        response = {"detail": "Successfully logged out."}
        return Response(
            self.get_results(results_count=1, results=response),
            status=status.HTTP_200_OK,
        )


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
