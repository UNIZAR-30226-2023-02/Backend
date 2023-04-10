# lobby/consumers.py
import json
from trivial_api.models import *
from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer



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


class lobbyConsumer(WebsocketConsumer):
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

    # Receive message from WebSocket. Este es el mensaje en json que me envia el frontend
    #{message: "Hola que tal"}
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "lobby_message", "message": message}
        )

    # Receive message from room group
    def lobby_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

"""
class GameConsumers(WebsocketConsumer):
    def connect(self):
        
        ###TODO
        #Calcular numero de usuarios conectados, si es 6 o igual a el numero de jugdores en la sala anteriro se empieza
        self.accept()
    
    def disconnect(self, close_code):
        # Leave room group
        print("")
        

    def gestionar_mensaje_entrante(self, text_data_json, fin):

        response = {

            'OK':"",
            'jugador':"",
            'type':"",
            'subtype': "",
            'valor_dado': "",
            'casilla_anterior': "",
            'casilla_elegida': "",
            'casillas_nuevas': "",
            'pregunta': "",
            'r1': "",
            'r2': "",
            'r3': "",
            'r4': "",
            'RC': "",
            'queso': "",
            'esCorrecta': "",
            'mensage_chat': "",
            'error': "",
        }

        if text_data_json["OK"] == "true":
            if text_data_json["type"] == "Peticion":
                if text_data_json["subtype"] == "Tirar_dado":
                    tirada = tirar_dado()###TODO
                    casillas_posibles = calcular_sig_movimiento(tirada, text_data_json["casilla_anterior"])###TODO
                    response['valor_dado'] = tirada
                    response['jugador'] = text_data_json["jugador"]
                    response['casillas_nuevas'] = casillas_posibles
                    response['type'] = "Respuesta"
                    response['subtype'] = "Dado_casillas"

                elif text_data_json["subtype"] == "Movimiento_casilla":
                    pregunta = elegir_pregunta(text_data_json["casilla_elegida"])###TODO
                    response['pregunta'] = pregunta[0]
                    response['r1'] = pregunta[1]
                    response['r2'] = pregunta[2]
                    response['r3'] = pregunta[3]
                    response['r4'] = pregunta[4]
                    response['RC'] = pregunta[5]
                    response['queso'] = pregunta[6]
                    response['jugador'] = text_data_json["jugador"]
                    response['type'] = "Respuesta"
                    response['subtype'] = "Pregunta"
                
            elif text_data_json["type"] == "Actualizacion":
                if text_data_json["esCorrecta"] == "true":
                    fin = False
                    if text_data_json["queso"] != "false":
                        fin = marcar_queso(text_data_json["queso"])###TODO

                    response['jugador'] = text_data_json["jugador"]
                    if fin == True:
                        response['type'] = "Fin"
                    else:
                        response['type'] = "Accion"
                        response['subtype'] = "Dados"
                elif text_data_json["esCorrecta"] == "false":
                    response['jugador'] = calcular_sig_jugador(text_data_json["jugador"])###TODO
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
            response['error'] = text_data_json["error"]

        return json.dumps(response)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        fin = False
        response = self.gestionar_mensaje_entrante(text_data_json, fin)

        if fin == False:
            self.send(response)
        else:
            self.close()
"""