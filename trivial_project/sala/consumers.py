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




#/ws/lobby/<room_name>/?token=Pepe2212&password=12345
class SalaConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "lobby_%s" % self.room_name
        
        # Get the query parameters from the URL
        query_params = parse_qs(self.scope["query_string"].decode())
        
        # Get the token and password parameters from the query parameters
        username = query_params.get("username", [None])[0]
        password = query_params.get("password", [None])[0]
        nombre_sala = self.room_name
        self.username = username

        sala = Sala.objects.filter(nombre_sala=self.room_name).first() or None
        user = Usuario.objects.filter(username=username).first() or None
        print(sala)
        print(user)
        print(username,password,nombre_sala)
        #Check if sala exists
        if sala and user:
            usuario_en_sala = UsuariosSala.objects.filter(username=user).first() or None
            #Check if the user is already in a sala
            if(not usuario_en_sala):
                jugadores_en_partida =  UsuariosSala.objects.filter(nombre_sala=nombre_sala).count()
                if(jugadores_en_partida >= sala.n_jugadores):
                    print("Hay muchos usuarios")
                    self.close()
                    return None
                if(sala.tipo_sala == "Privado"):
                    if(not sala.check_password(password)):
                        print("No coincide la contraseña")
                        self.close()
                        return None
            else:
                print("El usuario ya esta en la sala")
                self.close()
                return None                
        else:
            print("No existe sala ni usuario")
            self.close()
            return None

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        sala_usuario = UsuariosSala.objects.create(nombre_sala = sala, username=user)
        sala_usuario.save()
        self.accept()

        async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name, {"type": "actualizar_lista", "username": username}
                )

        sala = Sala.objects.filter(nombre_sala=self.room_name).first() or None

        if len(self.channel_layer.groups.get(self.room_group_name, {}).items()) == sala.n_jugadores:

            orden = lista_usuarios_sala(self.room_name)

            partida = Partida.objects.create(tipo=sala.tipo_partida,terminada=False,orden_jugadores=orden)

            wspartida = "/ws/partida/" + str(partida.id) + "/"
            
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "comenzar_partida", "wspartida": wspartida }
            )

        
    def disconnect(self, close_code):
        # Send message to WebSocket
        sala = Sala.objects.filter(nombre_sala=self.room_name).first() or None
        if(sala):
            usuario_sala = UsuariosSala.objects.filter(nombre_sala=self.room_name,username = self.username).first() or None
            if(usuario_sala):
                usuario_sala.delete()

            self.send(text_data=json.dumps({"Error":"Desconectado"}))

            # Si el creador abandona la sala se elimina la sala.
            if(self.username == str(sala.creador_username)):
                # Envio mensaje a todos los demás de desconexión
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": "sala_cancelada"}
                )
                self.close()
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {"type": "actualizar_lista"}
                )
                # Django elimina al usuario del grupo
                async_to_sync(self.channel_layer.group_discard)(
                    self.room_group_name, self.channel_name
                )
                self.close()
            # Si no hay jugadores en la sala, esta se elimina
            usuarios_sala = UsuariosSala.objects.filter(nombre_sala=self.room_name).first() or None
            if not usuarios_sala:
                sala.delete()


    def comenzar_partida(self, event):
        self.send(text_data=json.dumps({"accion": "empezar_partida", "url_partida": event["wspartida"]}))
        self.disconnect(0)

    def sala_cancelada(self,event):
        self.send(text_data=json.dumps({"accion": "actualizar_lista", "usernames": lista_usuarios_sala(self.room_name)}))
        self.disconnect(0)

    def actualizar_lista(self, event):
        # Send message to WebSocket, to the Frontend
        self.send(text_data=json.dumps({"accion": "actualizar_lista", "usernames": lista_usuarios_sala(self.room_name)}))