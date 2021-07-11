import logging

from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # TODO update to handle different type of error
    if response is not None:
        data = response.data

        response.data = {}
        errors = []

        for field, value in data.items():
            errors.append(prepare_error_message(field, value))
        response.data["message"] = errors[0] if len(errors) > 0 else ""
        response.data["code"] = response.status_code

    return response


def prepare_error_message(key, value):
    message = None
    if isinstance(value, str):
        message = f"{value}"
    elif isinstance(value, list):
        message = f"{key}: {''.join(value)}"
    elif isinstance(value, dict):
        nested_key = list(value.keys())[0]
        nested_value = list(value.values())[0]
        new_key = f"{key}.{nested_key}"
        message = prepare_error_message(new_key, nested_value)

    return message
