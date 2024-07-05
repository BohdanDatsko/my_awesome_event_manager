from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response

from my_awesome_event_manager.api.mixins import BaseMixin
from my_awesome_event_manager.core.decorators import calculate_api_time

User = get_user_model()


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class UserMixin(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, BaseMixin):
    @calculate_api_time
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return Response(
            self.get_list_results(response_data=response.data),
            status=status.HTTP_200_OK,
        )

    @calculate_api_time
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            self.get_results(results_count=1, results=response.data),
            status=status.HTTP_200_OK,
        )

    @calculate_api_time
    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        response = super().update(request, *args, **kwargs)
        return Response(
            self.get_results(results_count=1, results=response.data),
            status=status.HTTP_200_OK,
        )


# ------------------------------------------------------ #
# ------------------------------------------------------ #


class UserUUIDMixin(RetrieveModelMixin, BaseMixin):
    @calculate_api_time
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            self.get_results(results_count=1, results=response.data),
            status=status.HTTP_200_OK,
        )


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
