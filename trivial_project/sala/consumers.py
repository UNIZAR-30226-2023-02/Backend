# lobby/consumers.py
import json
from trivial_api.models import *
from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from trivial_api.funciones_auxiliares import *

class SalaConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "lobby_%s" % self.room_name

        #Comprobamos si la sala existe, en caso de que no exista denegamos el acceso
        if not Sala.objects.filter(nombre_sala=self.room_name).exists():
            #Esto no se puede enviar ya que no se ha aceptado la conexion, por lo que no hay canal
            # async_to_sync(
            #     self.send(text_data=json.dumps)({"message": "No puedes conectarte"})
            # )
            self.close()
            return
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()
        
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

#Envia el mensaje con el usuario al frontend
class lobbyConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "lobby_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Send message to WebSocket
        self.send(text_data=json.dumps({"Error":"Desconectado"}))
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        self.close()

    # Receive message from WebSocket. Este es el mensaje en json que me envia el frontend
    #{message: "Hola que tal"}
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        token = text_data_json["token"]
        username = get_username_by_token(token)
        if(username):
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "tirar_dado", "tirada": 2,"username": username}
            )
        else:
            # Send message to WebSocket
            self.disconnect(0)

    # Receive message from room group
    def lobby_message(self, event):
        username = event["username"]
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"username":username,"message": message}))
    
        # Receive message from room group
    def tirar_dado(self, event):
        username = event["username"]
        tirada = event["tirada"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"username":username,"tirada": tirada}))
