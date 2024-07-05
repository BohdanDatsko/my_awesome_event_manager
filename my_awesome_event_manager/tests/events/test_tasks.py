from unittest.mock import Mock
from unittest.mock import patch

from my_awesome_event_manager.events.models import Event
from my_awesome_event_manager.events.tasks import send_invitation_email

# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


@patch("my_awesome_event_manager.events.tasks.send_mail")
@patch("my_awesome_event_manager.events.tasks.get_object_or_404")
def test_send_invitation_email_success(mock_get_object_or_404, mock_send_mail):
    # Arrange
    mock_event = Mock(spec=Event)
    mock_event.title = "Test Event"
    mock_event.date = "2022-01-01"
    mock_event.location = "Test Location"
    mock_event.description = "Test Description"
    mock_get_object_or_404.return_value = mock_event

    event_id = 1
    from_email = "test@example.com"
    to_emails = ["test1@example.com", "test2@example.com"]

    # Act
    result = send_invitation_email(event_id, from_email, to_emails)

    # Assert
    mock_get_object_or_404.assert_called_once_with(Event, event_id=event_id)
    mock_send_mail.assert_called_once_with(
        f"Invitation to {mock_event.title}",
        f"You are invited to {mock_event.title} on {mock_event.date} at {mock_event.location}. \n\nDescription: {mock_event.description}",
        from_email,
        [to_emails],
    )
    assert result == {"status": "success", "message": "Invitation email has been sent"}


@patch("my_awesome_event_manager.events.tasks.send_mail")
@patch("my_awesome_event_manager.events.tasks.get_object_or_404")
def test_send_invitation_email_failure(mock_get_object_or_404, mock_send_mail):
    # Arrange
    mock_send_mail.side_effect = Exception("Test exception")
    mock_get_object_or_404.return_value = Mock(spec=Event)

    event_id = 1
    from_email = "test@example.com"
    to_emails = ["test1@example.com", "test2@example.com"]

    # Act
    result = send_invitation_email(event_id, from_email, to_emails)

    # Assert
    assert result == {"status": "error", "message": "Failed to send invitation email"}


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
