from django.test import TestCase

from my_awesome_event_manager.events.models import Event, EventParticipant
from my_awesome_event_manager.tests.events.factories import (
    EventFactory,
    EventParticipantFactory,
)
from my_awesome_event_manager.tests.users.factories import UserFactory


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class EventTests(TestCase):
    @staticmethod
    def create_event() -> Event:
        organizer = UserFactory()
        return EventFactory(organizer=organizer)

    def test_create_event(self):
        event = self.create_event()

        self.assertTrue(isinstance(event, Event))
        self.assertEqual(event.__str__(), f"{event.event_id}: {event.title}")

    def test_update_event(self):
        event = self.create_event()
        event.title = "UPDATED"
        event.save()

        self.assertEqual(Event.objects.filter(title="UPDATED").count(), 1)

    def test_remove_event(self):
        event = self.create_event()
        event.delete()

        self.assertEqual(Event.objects.count(), 0)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class EventParticipantTests(TestCase):
    @staticmethod
    def create_event_participant() -> EventParticipant:
        user = UserFactory(email="participant@email.com")
        organizer = UserFactory(email="organizer@email.com")
        event = EventFactory(organizer=organizer)
        return EventParticipantFactory(event=event, user=user)

    def test_create_event_participant(self):
        event_participant = self.create_event_participant()

        self.assertTrue(isinstance(event_participant, EventParticipant))
        self.assertEqual(
            event_participant.__str__(),
            f"{event_participant.event_participant_id}: {event_participant.event.title} - {event_participant.user.email}",
        )

    def test_update_event_participant(self):
        event_participant = self.create_event_participant()
        event_participant.email = "UPDATED@email.com"
        event_participant.save()

        self.assertEqual(
            EventParticipant.objects.filter(email="UPDATED@email.com").count(), 1
        )

    def test_remove_event_participant(self):
        event_participant = self.create_event_participant()
        event_participant.delete()

        self.assertEqual(EventParticipant.objects.count(), 0)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
