# partida/consumers.py
#
# Fichero de configuración para el Websockets de las partidas
#

import json
from trivial_api.models import *
from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs

# Hay que poner partida.funciones_auxiliares no funciones_auxiliares
from .funciones_auxiliares import *

class GameConsumers(WebsocketConsumer):
    def connect(self):
        self.game_name = self.scope["url_route"]["kwargs"]["game_name"]
        self.game_group_name = "game_%s" % self.game_name

        # Get the query parameters from the URL
        query_params = parse_qs(self.scope["query_string"].decode())
        
        # Get the token and password parameters from the query parameters
        username = query_params.get("username", [None])[0]
        password = query_params.get("password", [None])[0]    
        self.username = username
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name, self.channel_name
        )

        game = Partida.objects.filter(id =self.game_name).first() or None
        # Si no existe el juego denegamos el acceso
        if not game:
            print("Error no game")
            return None
        # Si se ha acabado la partida tambien denegamos el acceso
        if game.terminada == True:
            print("Error partida terminada")
            return None
        
        self.accept()
       
        user = Usuario.objects.filter(username=username).first() or None
        # Si no existe el usuario denegamos el acceso
        if not user:
            print("Error not user")
            return None
        # Si el usuario estaba desconectado entonces tengo que enviarselo solo a el
        juega = Juega.objects.filter(id_partida=game,username=user).first() or None

        # Si el que estaba jugando se ha desconectado y ha vuelto a entrar, entonces solo se lo envio a el
        print("Juega activo: ", str(juega.activo))
        if(juega and not juega.activo):
            datos_cargar_partida = cargar_datos_partida(self)
            self.send(text_data=json.dumps({'type': 'enviar_datos','datos': datos_cargar_partida}))
        else:
            print("Else")
            # Si estan los jugadores que se necesitan para iniciar la partida, entocnes le enviamos a todos los usuarios la informacion
            if len(self.channel_layer.groups.get(self.game_group_name, {}).items()) == calcular_jugadores(self.game_name):
                datos_cargar_partida = cargar_datos_partida(self)
                print("Empieza la partida")
                # Envio a todos los jugadores el mensaje 
                async_to_sync(self.channel_layer.group_send)(
                    self.game_group_name, {"type": "enviar_datos", "datos": datos_cargar_partida}
                )
        
    def enviar_datos(self, event):
        datos = event['datos']
        print(datos)
        self.send(text_data=json.dumps(datos))


    def disconnect(self, close_code):
        # Hacemos que el usuario no este activo
        juega = Juega.objects.filter(id_partida=self.game_name,username=self.username).first() or None
        juega.activo = False
        juega.save()
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name, self.channel_name
        )
        self.close()
    
    def receive(self, text_data):
        mensaje = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {"type": "gestionar.mensaje", "mensaje": mensaje}
        )
        

    def gestionar_mensaje(self, event):
        fin = False
        mensaje = event['mensaje']
        if mensaje['jugador'] != self.username:
            self.send(text_data=json.dumps(mensaje))
            return None

        response = {

            'OK':"",
            'jugador':"",
            'type':"",
            'subtype': "",
            'valor_dado': "",
            'casilla_elegida': "",
            'casillas_nuevas': "",
            'enunciado': "",
            'r1': "",
            'r2': "",
            'r3': "",
            'r4': "",
            'rc': "",
            'quesito': "",
            'esCorrecta': "",
            'mensage_chat': "",
            'error': "",
        }

        if mensaje['OK'] == "true":
            if mensaje['type'] == "Peticion":
                if mensaje['subtype'] == "Tirar_dado":
                    tirada = tirar_dado()
                    casillas_posibles = calcular_siguiente_movimiento(tirada, mensaje['jugador'], self.game_name)
                    response['valor_dado'] = tirada
                    response['jugador'] = mensaje['jugador']
                    response['casillas_nuevas'] = casillas_posibles
                    response['type'] = "Respuesta"
                    response['subtype'] = "Dado_casillas"

                elif mensaje['subtype'] == "Movimiento_casilla":
                    pregunta = elegir_pregunta(mensaje['casilla_elegida'], mensaje['jugador'], self.game_name)
                    if pregunta['enunciado'] == 'repetir':
                        response['type'] = "Accion"
                        response['subtype'] = "Dados"

                    else:
                        response['enunciado'] = pregunta['enunciado']
                        response['r1'] = pregunta['r1']
                        response['r2'] = pregunta['r2']
                        response['r3'] = pregunta['r3']
                        response['r4'] = pregunta['r4']
                        response['rc'] = pregunta['rc']
                        response['quesito'] = pregunta['tematica']
                        response['jugador'] = mensaje['jugador']
                        response['type'] = "Respuesta"
                        response['subtype'] = "Pregunta"
                
            elif mensaje['type'] == "Actualizacion":
                if mensaje['esCorrecta'] == "true":
                    if mensaje['quesito'] != "false":
                        fin = marcar_queso(mensaje['quesito'], mensaje['quesito'], self.game_name)

                    response['jugador'] = mensaje['jugador']
                    if fin == True:
                        response['type'] = "Fin"
                    else:
                        response['type'] = "Accion"
                        response['subtype'] = "Dados"
                elif mensaje['esCorrecta'] == "false":
                    response['jugador'] = calcular_sig_jugador(self.game_name)
                    response['type'] = "Accion"
                    response['subtype'] = "Dados"
                else:
                    print("")
            else:
                #Error el backend solo recive Peticiones y Actualizaciones
                print("")
            
            response['OK'] = "true"
        else:
            response['OK'] = "false"
            response['error'] = mensaje['error']

        if fin == False:

            self.send(text_data=json.dumps(response))
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name, {"type": "enviar_datos", "datos": response}
            )

        else:
            self.disconnect()


