from my_awesome_event_manager.core.permissions import IsApiAuthenticated


# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #


class IsRequestUserOrAdmin(IsApiAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "PUT"]:
            if request.user == obj or request.user.is_staff:
                return True
            return False
        return True


# ----------------------------------------------------------------- #
# ----------------------------------------------------------------- #
