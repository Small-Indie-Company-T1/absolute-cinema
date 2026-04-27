from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, ctx):
    response = exception_handler(exc, ctx)
    if response is not None:
        data = {
            'status': 'error',
            'code': response.status_code,
            'message': response.data
        }
        response.data = data
    return response
