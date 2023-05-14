# lobby/consumers.py
import json
from trivial_api.models import *
from sala.models import *
from partida.models import *
import random

from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from .funciones_auxiliares import *
from urllib.parse import parse_qs


#/ws/lobby/<room_name>/?username=Pepe2212&password=12345
class SalaConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "lobby_%s" % self.room_name
        
        # Get the query parameters from the URL
        query_params = parse_qs(self.scope["query_string"].decode())
        
        # Get the username and password parameters from the query parameters
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
            peticion = PeticionesAmigo.objects.filter(user=user,sala_inv=sala).first() or None
            usuario_en_sala = UsuariosSala.objects.filter(username=user, nombre_sala=nombre_sala).first() or None
            #Check if the user is already in a sala
            if(not usuario_en_sala):
                jugadores_en_partida =  UsuariosSala.objects.filter(nombre_sala=nombre_sala).count()
                if(jugadores_en_partida >= sala.n_jugadores):
                    print("Hay muchos usuarios")
                    self.close()
                    return None
                # Si es privada y no tengo peticion, entonces no puedo entrar sin la contraseña
                # Si tengo la peticion puedo entrar directamente
                if(sala.tipo_sala == "Privado" and not peticion):
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

        # Cuando esten todos los jugadores iniciamos la partida
        if len(self.channel_layer.groups.get(self.room_group_name, {}).items()) == sala.n_jugadores:
            # Generamos el orden aleatorio de los jugadores
            orden_aleatorio = usuarios_orden_aleatorio(self.room_name, sala.tipo_partida)
            # Creamos la partida
            partida = Partida.objects.create(tipo=sala.tipo_partida,terminada=False,tiempo_respuesta=sala.tiempo_respuesta,orden_jugadores=orden_aleatorio, orden_jugadores_inicial=orden_aleatorio)
            # Creamos la instancia de juega para los jugadores
            generar_jugadores(partida,sala.tipo_partida)
            if sala.tipo_partida == "Clasico":
                wspartida = "/ws/partida/" + str(partida.id) + "/"
            elif sala.tipo_partida == "Tematico":
                wspartida = "/ws/partida_tematico/" + str(partida.id) + "/"
                partida.tematica =  sala.tematica
                partida.save()
            elif sala.tipo_partida == "Equipo":
                wspartida = "/ws/partida_equipo/" + str(partida.id) + "/"
                partida.save()
            
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "comenzar_partida", "wspartida": wspartida }
            )


        
    def disconnect(self, close_code):
        # Send message to WebSocket
        sala = Sala.objects.filter(nombre_sala=self.room_name).first() or None
        if(not sala):
            self.close()
            return
        usuario_sala = UsuariosSala.objects.filter(nombre_sala=sala,username = self.username).first() or None
        if(usuario_sala):
            usuario_sala.delete()

        self.send(text_data=json.dumps({"Error":"Desconectado"}))

            
        # Si el creador abandona la sala se elimina la sala.
        if(self.username == str(sala.creador_username)):
            # Envio mensaje a todos los demás de desconexión
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "sala_cancelada"}
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "actualizar_lista"}
            )

            # Django elimina al usuario del grupo
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name
            )

        # Si no hay jugadores en la sala, esta se elimina
        usuarios_sala = UsuariosSala.objects.filter(nombre_sala=self.room_name).first() or None
        if not usuarios_sala:
            sala.delete()
        self.close()


    def comenzar_partida(self, event):
        self.send(text_data=json.dumps({"accion": "empezar_partida", "url_partida": event["wspartida"]}))
        # TODO esto no estaba ya que no desconectaba
        #self.disconnect(0)

    def sala_cancelada(self,event):
        self.send(text_data=json.dumps({"accion": "actualizar_lista", "usernames": lista_usuarios_sala(self.room_name)}))
        #self.disconnect(0)

    def actualizar_lista(self, event):
        # Send message to WebSocket, to the Frontend
        self.send(text_data=json.dumps({"accion": "actualizar_lista", "usernames": lista_usuarios_sala(self.room_name)}))