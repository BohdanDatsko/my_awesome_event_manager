from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response

from my_awesome_event_manager.api.mixins import BaseMixin
from my_awesome_event_manager.core.decorators import calculate_api_time
from my_awesome_event_manager.events.tasks import send_invitation_email_task

User = get_user_model()


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class EventListCreateMixin(ListModelMixin, CreateModelMixin, BaseMixin):
    @calculate_api_time
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return Response(
            self.get_list_results(response_data=response.data),
            status=status.HTTP_200_OK,
        )

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @calculate_api_time
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if "participants" in request.data and isinstance(
            request.data.get("participants"),
            list,
        ):
            event_id = response.data.get("event_id", None)
            participants = request.data.get("participants")
            send_invitation_email_task(event_id, request.user.email, participants)

        return Response(
            self.get_results(results_count=1, results=response.data),
            status=status.HTTP_201_CREATED,
        )


# ------------------------------------------------------------- #
# ------------------------------------------------------------- #


class EventGetUpdateDeleteMixin(
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    BaseMixin,
):
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

    @calculate_api_time
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        super().destroy(request, *args, **kwargs)
        return Response(
            self.get_results(
                results_count=1,
                results={"message": f'Your event "{obj.title}" successfully deleted'},
            ),
            status=status.HTTP_204_NO_CONTENT,
        )


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
