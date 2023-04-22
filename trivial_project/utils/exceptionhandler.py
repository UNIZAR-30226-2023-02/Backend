from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
import traceback
from django.conf import settings

# Gestor personalizado para las excepciones.
def custom_exception_handler(exc, context):
    # En caso de que falle el token
    if isinstance(exc, AuthenticationFailed):
        response_data = {
            'error': 'Authentication Error',
            'message': 'Invalid or missing authorization header'
        }
        return JsonResponse(response_data, status=401)
    else:
        if settings.DEBUG:
            # default error message for other exceptions
            response_data = {
                'error': str(exc),
                'message': 'An unexpected error occurred'
            }
            # include traceback if DEBUG=True
            response_data['traceback'] = traceback.format_exc()
            return JsonResponse(response_data, status=500)
        else:
            response_data = {
                'error': 'An unexpected error occurred'
            }
            return JsonResponse(response_data, status=500)

        