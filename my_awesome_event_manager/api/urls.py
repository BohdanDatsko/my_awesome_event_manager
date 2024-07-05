from django.urls import include, path

from my_awesome_event_manager.api.auth import urls as auth_urls
from my_awesome_event_manager.api.users import urls as users_urls
from my_awesome_event_manager.api.events import urls as events_urls

# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #


app_name = "api"

# /api/...


urlpatterns = [
    # --------------------------- auth ---------------------------- #
    # ------------------------------------------------------------- #
    path("auth/", include(auth_urls)),
    # --------------------------- users --------------------------- #
    # ------------------------------------------------------------- #
    path("users/", include(users_urls)),
    # -------------------------- events --------------------------- #
    # ------------------------------------------------------------- #
    path("events/", include(events_urls)),
]


# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
