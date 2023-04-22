from django.urls import re_path 
from . import consumers

websocket_urlpatterns = [
    re_path(r"partida/(?P<room_name>\w+)/$", consumers.GameConsumers.as_asgi()),
]