from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "my_awesome_event_manager.api"
    verbose_name = "API"

    def ready(self):
        try:
            import my_awesome_event_manager.api.signals  # noqa F401
        except ImportError:
            pass
