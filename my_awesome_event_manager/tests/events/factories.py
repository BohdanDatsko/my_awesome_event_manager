from datetime import datetime

import factory
from factory import Faker
from factory.django import DjangoModelFactory

from my_awesome_event_manager.events.models import Event, EventParticipant
from my_awesome_event_manager.tests.users.factories import UserFactory


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class EventFactory(DjangoModelFactory):
    title = Faker("name")
    description = Faker("text")
    date = Faker("date_time")
    location = Faker("address")
    organizer = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(datetime.now)
    updated_at = Faker("date_time")

    class Meta:
        model = Event


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class EventParticipantFactory(DjangoModelFactory):
    event = factory.SubFactory(EventFactory)
    user = factory.SubFactory(UserFactory)
    email = Faker("email")
    is_confirmed = Faker("boolean")

    class Meta:
        model = EventParticipant


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
