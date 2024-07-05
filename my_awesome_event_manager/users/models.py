import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from my_awesome_event_manager.users.managers import UserManager


# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #


class User(AbstractUser):
    """
    Default custom user model for My Awesome Event Manager.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    user_id = models.UUIDField(
        default=uuid.uuid4,
        null=True,
        blank=True,
        unique=True,
        editable=False,
    )
    first_name = CharField(_("First name"), blank=True, max_length=255)
    last_name = CharField(_("Last name"), blank=True, max_length=255)
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("api:user_by_id", kwargs={"user_id": self.user_id})


# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
