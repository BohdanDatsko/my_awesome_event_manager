import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404

from my_awesome_event_manager.events.models import Event

User = get_user_model()


# Get the Celery logger
logger = logging.getLogger("celery.worker")
logger.propagate = True


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


def send_invitation_email(event_id, from_email, to_emails):
    try:
        event = get_object_or_404(Event, event_id=event_id)
        subject = f"Invitation to {event.title}"
        message = (
            f"You are invited to {event.title} on {event.date} at {event.location}. \n\n"
            f"Description: {event.description}"
        )
        send_mail(subject, message, from_email, [to_emails])
        logger.info(
            f"send_invitation_email: Invitation to '{event.title}' has been sent to {to_emails}",
        )
        return {"status": "success", "message": "Invitation email has been sent"}
    except Exception as e:
        logger.error(f"send_invitation_email: {e}")
        return {"status": "error", "message": "Failed to send invitation email"}


# -------------------------------------------- #
# -------------------------------------------- #


@shared_task(name="send_invitation_email_task")
def send_invitation_email_task(event_id, from_email, to_emails):
    send_invitation_email(event_id, from_email, to_emails)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
