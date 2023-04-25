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

# Hay que poner partida.funciones_auxiliares no funciones_auxiliares
from .funciones_auxiliares import *

class GameConsumers(WebsocketConsumer):
    def connect(self):
        self.game_name = self.scope["url_route"]["kwargs"]["game_name"]
        self.game_group_name = "game_%s" % self.game_name

        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name, self.channel_name
        )

        self.accept()
        ###generar_jugador()
        ###TODO
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name, self.channel_name
        )
    
    def receive(self, text_data):
        mensaje = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name, {"type": "gestionar.mensaje", "mensaje": mensaje}
        )
        

    def gestionar_mensaje(self, event):
        num_jugadores = 4
        fin = False
        mensaje = event['mensaje']
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
                    response['jugador'] = calcular_sig_jugador(self.game_name, num_jugadores)
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
        else:
            self.disconnect()


