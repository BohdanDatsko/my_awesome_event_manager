from rest_framework import status

# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


DICT_STATUS_CODES = {
    "invalid": status.HTTP_400_BAD_REQUEST,
    "required": status.HTTP_400_BAD_REQUEST,
    "parse_error": status.HTTP_400_BAD_REQUEST,
    "authentication_failed": status.HTTP_401_UNAUTHORIZED,
    "not_authenticated": status.HTTP_401_UNAUTHORIZED,
    "permission_denied": status.HTTP_403_FORBIDDEN,
    "not_found": status.HTTP_404_NOT_FOUND,
    "method_not_allowed": status.HTTP_405_METHOD_NOT_ALLOWED,
    "not_acceptable": status.HTTP_406_NOT_ACCEPTABLE,
    "unsupported_media_type": status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    "throttled": status.HTTP_429_TOO_MANY_REQUESTS,
}


# --------------------------------------------------- #
# --------------------------------------------------- #


class GeneratedAnswerType:
    gpt_vision = "gpt_vision"
    rivet = "rivet"


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
