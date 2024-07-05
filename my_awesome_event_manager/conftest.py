import pytest

from my_awesome_event_manager.events.models import Event, EventParticipant
from my_awesome_event_manager.tests.events.factories import EventFactory, EventParticipantFactory
from my_awesome_event_manager.users.models import User
from my_awesome_event_manager.tests.users.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture()
def user(db) -> User:
    return UserFactory()


@pytest.fixture()
def event(db) -> Event:
    return EventFactory()


@pytest.fixture()
def event_participant(db) -> EventParticipant:
    return EventParticipantFactory()
