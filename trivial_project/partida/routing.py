from django.urls import re_path 
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/partida/(?P<game_name>\w+)/$", consumers.GameConsumers.as_asgi()),
]