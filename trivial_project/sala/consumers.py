# lobby/consumers.py
import json
from trivial_api.models import *
from sala.models import *
from partida.models import *

from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from .funciones_auxiliares import *
from urllib.parse import parse_qs





class SalaConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "lobby_%s" % self.room_name
        query_params = parse_qs(self.scope["query_string"].decode())
        username = query_params["token"][-1]

        sala = Sala.objects.filter(nombre_sala=self.room_name).first() or None
        user = Usuario.objects.filter(username=username).first() or None
        #Check if sala and user exists
        if sala and user:
            #Check if the user is already in a sala
            print ("El usuaio existe: " + str(UsuariosSala.objects.filter(username=user).exists()))
            if(not UsuariosSala.objects.filter(username=user, nombre_sala=self.room_name).exists()):
                jugadores_en_partida =  UsuariosSala.objects.filter(nombre_sala=self.room_name).count()
                if(jugadores_en_partida > sala.n_jugadores):
                    self.close()
                    return None
            else:
                self.close()
                return None    
        else:
            self.close()
            return None



        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        # Unimos el usuario a la sala
        sala_usuario = UsuariosSala.objects.create(nombre_sala = sala, username=user)
        sala_usuario.save()

        self.accept()

        async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "nuevo.usuario", "username": username}
        )
        
        
    def disconnect(self, close_code):
        # Send message to WebSocket
        self.send(text_data=json.dumps({"Error":"Desconectado"}))
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        self.close()

    # Receive message from WebSocket. Este es el mensaje en json que me envia el frontend
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        accion = text_data_json["accion"]
        query_params = parse_qs(self.scope["query_string"].decode())
        username = query_params["token"][-1]
        
        sala = Sala.objects.filter(nombre_sala=self.room_name).first() or None


        if sala and str(sala.creador_username) == username and accion == "empezar":
        
            orden = lista_usuarios_sala(self.room_name)
            print ("El orden es: " + str(orden))



            partida = Partida.objects.create(tipo=sala.tipo_partida,terminada=False,orden_jugadores=orden)

            wspartida = "/ws/partida/" + str(partida.id) + "/"
            
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "comenzar.partida", "wspartida": wspartida }
            )
        else:
            print(sala.creador_username,username,accion)
            # Send message to WebSocket
            self.send(text_data=json.dumps({"accion": "error", "mensaje": "No tienes permiso para comenzar la partida"}))

    def comenzar_partida(self, event):
        
        self.send(text_data=json.dumps({"accion": "empezar_partida", "url_partida": event["wspartida"]}))
        self.disconnect(0)


    def nuevo_usuario(self, event):
        username = event["username"]
        # Send message to WebSocket, to the Frontend
        self.send(text_data=json.dumps({"accion": "nuevo_usuario", "username": lista_usuarios_sala(self.room_name)}))

        
         

