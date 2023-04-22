# partida/consumers.py
#
# Fichero de configuración para el Websockets de las partidas
#

import json
from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from funciones_auxiliares import *

class GameConsumers(WebsocketConsumer):
    def connect(self):
        
        self.accept()
        generar_jugador()
        ###TODO
    
    def disconnect(self, close_code):
        # Leave room group
        print("")
        
'''
    def gestionar_mensaje_entrante(self, text_data_json, fin):
        id_partida = 1
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

        if text_data_json('OK') == "true":
            if text_data_json('type') == "Peticion":
                if text_data_json('subtype') == "Tirar_dado":
                    tirada = tirar_dado()
                    casillas_posibles = calcular_siguiente_movimiento(tirada, text_data_json('jugador'), id_partida)
                    response['valor_dado'] = tirada
                    response['jugador'] = text_data_json('jugador')
                    response['casillas_nuevas'] = casillas_posibles
                    response['type'] = "Respuesta"
                    response['subtype'] = "Dado_casillas"

                elif text_data_json('subtype') == "Movimiento_casilla":
                    pregunta = elegir_pregunta(text_data_json('casilla_elegida'), text_data_json('jugador'), id_partida)
                    response['enunciado'] = pregunta['enunciado']
                    response['r1'] = pregunta['r1']
                    response['r2'] = pregunta['r2']
                    response['r3'] = pregunta['r3']
                    response['r4'] = pregunta['r4']
                    response['rc'] = pregunta['rc']
                    response['quesito'] = pregunta['tematica']
                    response['jugador'] = text_data_json('jugador')
                    response['type'] = "Respuesta"
                    response['subtype'] = "Pregunta"
                
            elif text_data_json('type') == "Actualizacion":
                if text_data_json('esCorrecta') == "true":
                    fin = False
                    if text_data_json('quesito') != "false":
                        fin = marcar_queso(text_data_json('quesito'), text_data_json('jugador'), id_partida)

                    response['jugador'] = text_data_json('jugador')
                    if fin == True:
                        response['type'] = "Fin"
                    else:
                        response['type'] = "Accion"
                        response['subtype'] = "Dados"
                elif text_data_json('esCorrecta') == "false":
                    response['jugador'] = calcular_sig_jugador(id_partida)
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
            response['error'] = text_data_json('error')

        return response#json.dumps(response)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        fin = False
        response = self.gestionar_mensaje_entrante(text_data_json, fin)

        if fin == False:
            self.send(response)
        else:
            self.close()
'''
