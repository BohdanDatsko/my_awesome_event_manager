from dateutil.parser import parse
from django.urls import reverse
from rest_framework import status

from my_awesome_event_manager.events.models import EventParticipant
from my_awesome_event_manager.tests.events.factories import EventFactory
from my_awesome_event_manager.tests.utils.base_test_setup import BaseAPITestCase

# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class EventListCreateTest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.organizer = self.user
        self.event = EventFactory(organizer=self.organizer)
        self.url = reverse("api:events:events")

    def test_list_events(self):
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.json().get("results"), [])

    def test_list_events_with_date_filter(self):
        # Create events with different dates
        EventFactory(organizer=self.organizer, date="2024-07-07")
        EventFactory(organizer=self.organizer, date="2024-07-08")

        def test_date_filter(date_str, expected_date):
            # Test filtering by date
            response = self.client.get(
                self.url + "?date=" + date_str,
                **self.auth_headers,
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.json().get("results")), 1)
            response_date = parse(response.json().get("results")[0].get("date")).date()
            self.assertEqual(response_date.isoformat(), expected_date)

        test_date_filter("2024-07-07", "2024-07-07")
        test_date_filter("July 7, 2024", "2024-07-07")

    def test_list_events_with_search_filter(self):
        # Create events with different titles and locations
        EventFactory(
            organizer=self.organizer,
            title="Test Event 1",
            location="Location 1",
        )
        EventFactory(
            organizer=self.organizer,
            title="Test Event 2",
            location="Location 2",
        )

        # Test searching by title
        response = self.client.get(self.url + "?search=Event 1", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 1)
        self.assertEqual(response.json().get("results")[0].get("title"), "Test Event 1")

        # Test searching by location
        response = self.client.get(self.url + "?search=Location 2", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 1)
        self.assertEqual(
            response.json().get("results")[0].get("location"),
            "Location 2",
        )

    def test_list_events_with_date_and_search_filters(self):
        # Create events with different dates, titles, and locations
        EventFactory(
            organizer=self.organizer,
            date="2024-07-07",
            title="Test Event 1",
            location="Location 1",
        )
        EventFactory(
            organizer=self.organizer,
            date="2024-07-08",
            title="Test Event 2",
            location="Location 2",
        )

        # Test filtering by date and searching by title
        response = self.client.get(
            self.url + "?date=2024-07-07&search=Event 1",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 1)
        self.assertEqual(response.json().get("results")[0].get("title"), "Test Event 1")
        response_date = parse(response.json().get("results")[0].get("date")).date()
        self.assertEqual(response_date.isoformat(), "2024-07-07")

        # Test filtering by date and searching by location
        response = self.client.get(
            self.url + "?date=2024-07-08&search=Location 2",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 1)
        self.assertEqual(
            response.json().get("results")[0].get("location"),
            "Location 2",
        )
        response_date = parse(response.json().get("results")[0].get("date")).date()
        self.assertEqual(response_date.isoformat(), "2024-07-08")

    def test_list_events_forbidden(self):
        response = self.client.get(self.url, **self.fake_auth_headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_event(self):
        response = self.client.post(
            self.url,
            {
                "title": "Test Event",
                "description": "Test Description",
                "date": "2024-07-07",
                "location": "Test Location",
            },
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_without_date_bad_request(self):
        response = self.client.post(
            self.url,
            {
                "title": "Test Event",
                "description": "Test Description",
                "location": "Test Location",
            },
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("error").get("message"),
            "'date' - This field is required.",
        )

    def test_create_event_with_participants(self):
        response = self.client.post(
            self.url,
            {
                "title": "Test Event",
                "description": "Test Description",
                "date": "2024-07-07",
                "location": "Test Location",
                "participants": ["test1@email.com", "test2@email.com"],
            },
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            EventParticipant.objects.filter(
                event__event_id=response.data.get("results").get("event_id"),
            ).count(),
            2,
        )


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class EventGetUpdateDeleteTest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.organizer = self.user
        self.event = EventFactory(organizer=self.organizer)
        self.url = reverse(
            "api:events:event_by_id",
            kwargs={"event_id": self.event.event_id},
        )

    def test_get_event_by_id(self):
        response = self.client.get(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_event_by_id_forbidden(self):
        response = self.client.get(self.url, **self.fake_auth_headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_event_by_id(self):
        response = self.client.put(
            self.url,
            {"title": "Test Event (UPDATED)"},
            format="json",
            **self.auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("results").get("title"),
            "Test Event (UPDATED)",
        )

    def test_update_event_by_id_forbidden(self):
        response = self.client.put(
            self.url,
            {"title": "Test Event (UPDATED)"},
            format="json",
            **self.fake_auth_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_event_by_id_without_body(self):
        response = self.client.put(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_event_by_id(self):
        response = self.client.delete(self.url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_event_by_id_forbidden(self):
        response = self.client.delete(self.url, **self.fake_auth_headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
