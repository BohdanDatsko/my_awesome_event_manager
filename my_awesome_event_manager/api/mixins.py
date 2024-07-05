from rest_framework.exceptions import ErrorDetail
from rest_framework.viewsets import GenericViewSet

from my_awesome_event_manager.contrib.choices.base import DICT_STATUS_CODES


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


class BaseMixin(GenericViewSet):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code not in [200, 201, 204]:
            error, error_code, error_message = None, None, None
            response = super().finalize_response(request, response, *args, **kwargs)
            if response.data.get("error", None):
                pass
            elif response.data.get("non_field_errors", None):
                if isinstance(response.data.get("non_field_errors", None)[0], ErrorDetail):
                    error = response.data.get("non_field_errors", None)[0]
                    error_code = error.code
                    error_message = error
            elif response.data.get("detail", None):
                if isinstance(response.data.get("detail", None), ErrorDetail):
                    error = response.data.get("detail", None)
                    error_code = error.code
                    error_message = error
            elif not response.data.get("results", None):
                for key, value in response.data.items():
                    if isinstance(value, list):
                        if value:
                            if isinstance(value[0], ErrorDetail):
                                error = value[0]
                                error_code = error.code
                                error_message = f"'{key}' - {value[0]}"
                    elif isinstance(value, dict):
                        if value:
                            for k, v in value.items():
                                if v:
                                    if isinstance(v[0], ErrorDetail):
                                        error = v[0]
                                        error_code = error.code
                                        error_message = f"'{key}[{k}]' - {v[0]}"
            if error:
                new_data = {
                    "status": "error",
                    "error": {
                        "code": DICT_STATUS_CODES.get(error_code, 400),
                        "message": error_message,
                    },
                }
                response.data = new_data
            return response
        return super().finalize_response(request, response, *args, **kwargs)

    @staticmethod
    def get_error(message):
        return {
            "status": "error",
            "error": {
                "code": DICT_STATUS_CODES.get("invalid", 500),
                "message": message,
            },
        }

    @staticmethod
    def get_results(
        results_count: int = None,
        previous_page: str = None,
        next_page: str = None,
        results: dict = None,
    ):
        return {
            "status": "ok",
            "results_time": "0 sec.",
            "results_count": results_count if results_count else 0,
            "next": next_page if next_page else None,
            "previous": previous_page if previous_page else None,
            "results": results if results else {},
        }

    @staticmethod
    def get_list_results(
        response_data: dict = None,
    ):
        return {
            "status": "ok",
            "results_time": "0 sec.",
            "results_count": response_data.get("count", 0),
            "next": response_data.get("next", None),
            "previous": response_data.get("previous", None),
            "results": response_data.get("results", []),
        }


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #
