from django.urls import path

from my_awesome_event_manager.api.events.views import EventGetUpdateDeleteView
from my_awesome_event_manager.api.events.views import EventListCreateView

app_name = "events"

# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #

# /api/auth/...


urlpatterns = [
    # URLs that do not require a session or valid token
    path(
        "",
        EventListCreateView.as_view({"get": "get", "post": "post"}),
        name="events",
    ),
    path(
        "<uuid:event_id>/",
        EventGetUpdateDeleteView.as_view(
            {"get": "get", "put": "put", "delete": "delete"},
        ),
        name="event_by_id",
    ),
]


# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
