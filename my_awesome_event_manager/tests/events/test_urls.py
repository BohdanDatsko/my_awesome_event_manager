import pytest
from django.urls import resolve
from django.urls import reverse

from my_awesome_event_manager.events.models import Event

pytestmark = pytest.mark.django_db


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


def test_list_create_events():
    assert reverse("api:events:events") == "/api/events/"
    assert resolve("/api/events/").view_name == "api:events:events"


def test_get_update_delete_event_by_id(event: Event):
    assert (
        reverse(
            "api:events:event_by_id",
            kwargs={"event_id": event.event_id},
        )
        == f"/api/events/{event.event_id}/"
    )
    assert (
        resolve(f"/api/events/{event.event_id}/").view_name == "api:events:event_by_id"
    )


# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
