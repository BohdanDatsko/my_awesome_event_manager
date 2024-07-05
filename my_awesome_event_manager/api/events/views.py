from dateutil.parser import parse
from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_spectacular.utils import extend_schema

from my_awesome_event_manager.api.events.mixins import EventGetUpdateDeleteMixin
from my_awesome_event_manager.api.events.mixins import EventListCreateMixin
from my_awesome_event_manager.api.events.serializers import EventCompactSerializer
from my_awesome_event_manager.api.events.serializers import EventSerializer
from my_awesome_event_manager.events.models import Event

User = get_user_model()


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class EventListCreateView(EventListCreateMixin):
    """
    API endpoint get or create events.

    ---
    get:
        Get multiple events.

        :param search: Search by title or location.
        :param date: Filter by date.

        Returns the compact event records for some filtered set of events.
        Use one or more of the parameters provided to filter the events returned.
    post:
        Create a new event.

        :param title: The event title. Required.
        :param date: The date when the event is going to be. Required.
        :param location: The location of the event. Required.
        :param participants: An array with emails of the possible participants. Optional.

        Returns the full record of the newly created event.
    """

    model = Event
    lookup_field = "event_id"
    lookup_url_kwarg = "event_id"
    queryset = Event.objects.all()
    serializer_classes = {
        "get": EventCompactSerializer,
        "post": EventSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    def parse_date(self, date_str):
        try:
            return parse(date_str).date()
        except ValueError:
            return None

    def get_queryset(self):
        queryset = super().get_queryset().select_related("organizer")
        search = self.request.GET.get("search", None)
        date_str = self.request.GET.get("date", None)

        if date_str is not None:
            date = self.parse_date(date_str)
            if date is not None:
                queryset = queryset.filter(date=date)

        if search is not None:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(location__icontains=search),
            )
        return queryset

    @extend_schema(tags=["Events API"], operation_id="events_get")
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["Events API"], operation_id="events_post")
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


# ------------------------------------------------------------- #
# ------------------------------------------------------------- #


class EventGetUpdateDeleteView(EventGetUpdateDeleteMixin):
    """
    API endpoint get, update or delete an event.

    ---
    get:
        Get an event.

        Returns the complete event record for a single event.
    put:
        Update an event.

        A specific, existing event can be updated by making a PUT request on the URL for that event.
        Only the fields provided in the data block will be updated; any unspecified fields will remain unchanged.

        When using this method, it is best to specify only those fields you wish to change,
        or else you may overwrite changes made by another user since you last retrieved the task.

        Returns the complete updated event record.
    delete:
        Delete an event.

        Returns an empty data record.
    """

    model = Event
    lookup_field = "event_id"
    lookup_url_kwarg = "event_id"
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        return super().get_queryset().select_related("organizer")

    @extend_schema(tags=["Events API"], operation_id="event_by_id_get")
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(tags=["Events API"], operation_id="event_by_id_put")
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(tags=["Events API"], operation_id="event_by_id_delete")
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
