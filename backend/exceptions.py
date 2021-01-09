import logging

from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data

        response.data = {}
        errors = []
        for field, value in data.items():
            errors.append("{} : {}".format(field, " ".join(value)))
        print(type(field))
        print(type(value))
        print(value)

        response.data["errors"] = errors
        # response.data['status'] = False

        response.data["exception"] = str(exc)

    return response
