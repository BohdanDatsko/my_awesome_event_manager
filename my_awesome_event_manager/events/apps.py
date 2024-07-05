import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EventsConfig(AppConfig):
    name = "my_awesome_event_manager.events"
    verbose_name = _("Events")

    def ready(self):
        with contextlib.suppress(ImportError):
            import my_awesome_event_manager.events.signals  # noqa: F401
