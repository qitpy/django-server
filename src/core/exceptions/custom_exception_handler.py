# custom handler
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        if getattr(exc, 'status_code', None) is not None:
            response.data['status_code'] = exc.status_code
        if getattr(exc, 'default_detail', None) is not None:
            response.data['default_detail'] = exc.default_detail
        if getattr(exc, 'default_code', None) is not None:
            response.data['default_code'] = exc.default_code

    return response
