from rest_framework.permissions import BasePermission

# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class IsApiAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if "Authorization" in request.headers:
            return bool(request.user and request.user.is_authenticated)
        return False


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
