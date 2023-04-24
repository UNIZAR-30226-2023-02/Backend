"""
ASGI config for conf_trivial_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
import sala.routing 
import partida.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf_trivial_project.settings')

django.setup()
application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                sala.routing.websocket_urlpatterns +
                partida.routing.websocket_urlpatterns
            )
        )
    ),
})
