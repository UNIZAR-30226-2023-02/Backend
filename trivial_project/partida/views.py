from django.shortcuts import render, get_object_or_404
from .models import *
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions,generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import re
from datetime import datetime

from partida.funciones_auxiliares import *

class Partida(APIView):
    def post(self, request):
        id_partida = 1
        response = {

            'OK':"",
            'jugador':"",
            'type':"",
            'subtype': "",
            'valor_dado': "",
            'casilla_anterior': "",
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

        if request.data.get('OK') == "true":
            if request.data.get('type') == "Peticion":
                if request.data.get('subtype') == "Tirar_dado":
                    tirada = tirar_dado()
                    casillas_posibles = calcular_siguiente_movimiento(tirada, request.data.get('casilla_anterior'))
                    response['valor_dado'] = tirada
                    response['jugador'] = request.data.get('jugador')
                    response['casillas_nuevas'] = casillas_posibles
                    response['type'] = "Respuesta"
                    response['subtype'] = "Dado_casillas"

                elif request.data.get('subtype') == "Movimiento_casilla":
                    pregunta = elegir_pregunta(request.data.get('casilla_elegida'))
                    response['enunciado'] = pregunta['enunciado']
                    response['r1'] = pregunta['r1']
                    response['r2'] = pregunta['r2']
                    response['r3'] = pregunta['r3']
                    response['r4'] = pregunta['r4']
                    response['rc'] = pregunta['rc']
                    response['quesito'] = pregunta['quesito']
                    response['jugador'] = request.data.get('jugador')
                    response['type'] = "Respuesta"
                    response['subtype'] = "Pregunta"
                
            elif request["type"] == "Actualizacion":
                if request["esCorrecta"] == "true":
                    fin = False
                    if request["queso"] != "false":
                        fin = marcar_queso(request["queso"], request["jugador"], id_partida)

                    response['jugador'] = request["jugador"]
                    if fin == True:
                        response['type'] = "Fin"
                    else:
                        response['type'] = "Accion"
                        response['subtype'] = "Dados"
                elif request["esCorrecta"] == "false":
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
            response['error'] = request["error"]

        return Response(response)#json.dumps(response)



# Create your views here.
