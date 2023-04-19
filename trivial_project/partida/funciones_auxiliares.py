#
#Fichero de funciones axuiliares para el transcrso de una partida
#

import json
from trivial_api.models import *
from Lib import random

# Función que devulve un valor aleatorio del 1-6 simulando la tirada de un dado
# @return string [1-6] 
def tirar_dado():

    return str(random.randint(1,6))


# Funcion que devuleve a que casillas puede llegar dados
#   una casilla y un numero de dado
# @param string(tirada [1-6])
# @param string(casilla [1-72])
# @return 
def calcular_siguiente_movimiento(tirada, ca):

    Casillas = ""
    for i in Tablero.objects.filter(casilla_actual=ca, tirada_dado=tirada).values_list('casilla_nueva'):
        Casillas = Casillas + "," + i
    return Casillas


# Elige una pregunta al hacer dependiendo de la casilla que se le pase
# Depende de la casilla sera de una tematica u otra
# @param casilla([1-72])
# @return vector(pregunta, r1, r2, r3, r4, rc, queso)
def elegir_pregunta(casilla):

    tematica = Casilla_Tematica.objects.values_list(tematica).filter(casilla = casilla)
    all_preguntas = Pregunta.objects.values_list('enunciado', 'r1', 'r2', 'r3', 'r4', 'rc', 'queso').filter(categoria = tematica)
    pregunta_devolver = all_preguntas[random.randint(1,len(all_preguntas))]

    return pregunta_devolver

# Marca el queso de la categoria que sea para el judaro dado y comprobar si es el ultimo queso
# @param queso([historia, arte, ciencia, geografia, entretenimiento, deportes])
# @param jugador(usernema)
# @return True si el jugador ha conseguido todos los quesos
def marcar_queso(queso, jugador):
    # TODO crear tabla Juega y actualizar el queso ganado al jugadro ganado
    # if queso == 'historia':
        
    # elif queso == 'arte':

    # elif queso == 'deportes':

    # elif queso == 'entretenimiento':

    # elif queso == 'ciencia':

    # elif queso == 'geografia': 
    return False   

# Calcula el siguente jugador a jugar dado el jugador que ha jugado en el ultimo turno
# @param jugador(username)
# @return jugador(username)
def calcular_sig_jugador(jugador_actual):
    # TODO Crear tabla partida y consultar el siguiente jugador
    
    
    return None