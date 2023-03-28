# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from trivial_api.models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        #Comprobamos si la sala existe
        if Sala.objects.filter(nombre_sala=self.room_name).exists():
            pass
        else:
            pass

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        #Si el numero de usuarios conectados en la sala es 0, entonces la eliminamos de la base de datos


    # Receive message from WebSocket. Este es el mensaje en json que me envia el frontend
    #{message: "Hola que tal"}
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
            "type": "chat_message", 
             "message": message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket. Esto es lo que vera el del frontend
        await self.send(text_data=json.dumps({"message": message}))