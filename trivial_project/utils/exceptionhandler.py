from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse

# Codigo necesario para que no salte excepcion en el caso
# de que el usuario no haya proporcionado un Token

def custom_exception_handler(request, exception):
    response_data = {
        'error': 'Authentication Error',
        'message': 'Invalid or missing authorization header'
    }
    return JsonResponse(response_data, status=401)