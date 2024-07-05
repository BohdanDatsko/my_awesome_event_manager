import logging
import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

logger = logging.getLogger("my_awesome_event_manager")

# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class Event(models.Model):
    """
    Event model for My Awesome Event Manager.
    """

    event_id = models.UUIDField(
        default=uuid.uuid4,
        null=True,
        blank=True,
        unique=True,
        editable=False,
    )
    title = models.CharField(max_length=256)
    description = models.CharField(blank=True, null=True, max_length=1024)
    date = (
        models.DateTimeField()
    )  # according to the different needs here also could be implemented a logic with start and end date
    location = models.CharField(max_length=256)
    organizer = models.ForeignKey(
        to=User,
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    # -------------------------------------------------- #
    # -------------------------------------------------- #

    class Meta:
        managed = True
        ordering = ["-created_at"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        try:
            return f"{self.event_id}: {self.title}"
        except Exception as e:
            logger.info(f"Event model __str__: {e}")
            return ""


# ------------------------------------------------------ #
# ------------------------------------------------------ #


class EventParticipant(models.Model):
    """
    EventParticipant model for My Awesome Event Manager.
    """

    event_participant_id = models.UUIDField(
        default=uuid.uuid4,
        null=True,
        blank=True,
        unique=True,
        editable=False,
    )
    event = models.ForeignKey(
        to=Event,
        null=True,
        blank=True,
        editable=False,
        on_delete=models.CASCADE,
    )
    email = models.EmailField(null=True, blank=True, default=None)
    user = models.ForeignKey(
        to=User,
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
    )
    is_confirmed = models.BooleanField(default=False)

    # -------------------------------------------------- #
    # -------------------------------------------------- #

    class Meta:
        managed = True
        ordering = ["-id"]
        verbose_name = "Event Participant"
        verbose_name_plural = "Event Participants"

    def __str__(self):
        try:
            user_email = self.user.email if self.user else self.email
            return (
                f"{self.event_participant_id}: {self.event.title} - {user_email}"
            )
        except Exception as e:
            logger.info(f"EventParticipant model __str__: {e}")
            return ""


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
