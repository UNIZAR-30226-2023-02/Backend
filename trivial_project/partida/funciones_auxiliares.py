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
    for i in Tablero.objects.filter(casilla_actual=ca, tirada_dado=tirada).values('casilla_nueva'):
        Casillas =  Casillas + str(i['casilla_nueva']) + ","
    
    Casillas = Casillas[:-1]
    return Casillas


# Elige una pregunta al hacer dependiendo de la casilla que se le pase
# Depende de la casilla sera de una tematica u otra
# @param casilla([1-72])
# @return vector(pregunta, r1, r2, r3, r4, rc)
def elegir_pregunta(casilla):

    inf_casilla = Casilla_Tematica.objects.filter(casilla = casilla).values('tematica', 'quesito').first()
    all_preguntas = Pregunta.objects.values('enunciado', 'r1', 'r2', 'r3', 'r4', 'rc').filter(categoria = inf_casilla['tematica'])
    pregunta_devolver = all_preguntas[random.randint(0,len(all_preguntas) - 1)]

    pregunta_devolver |= Casilla_Tematica.objects.filter(casilla = casilla).values('quesito').first()

    print(pregunta_devolver)
    return pregunta_devolver

# Marca el queso de la categoria que sea para el judaro dado y comprobar si es el ultimo queso
# @param queso([historia, arte, ciencia, geografia, entretenimiento, deportes])
# @param jugador(usernema)
# @Partida_id 
# @return True si el jugador ha conseguido todos los quesos
def marcar_queso(queso, jugador, Partida_id):
    
    juega = Juega.objects.filter(username = jugador, id_partida = Partida_id).first() or None
    
    if Partida == None:
        return 'Error, no existe partida'
    else:

        if queso == 'historia':
            if juega.q_historia == False:
                juega.q_historia = True
            
        elif queso == 'arte':
            if juega.q_arte == False:
                juega.q_arte = True

        elif queso == 'deportes':
            if juega.q_deporte == False:
                juega.q_deporte = True

        elif queso == 'entretenimiento':
            if juega.q_entretenimiento == False:
                juega.q_entretenimiento = True

        elif queso == 'ciencia':
            if juega.q_ciencia == False:
                juega.q_ciencia = True

        elif queso == 'geografia': 
            if juega.q_geografia == False:
                juega.q_geografia = True
        
        juega.save()
        if juega.q_geografia and juega.q_historia and juega.q_deporte and juega.q_ciencia and juega.q_arte and juega.q_entretenimiento:
            return True
        else:

             return False   

# Calcula el siguente jugador a jugar dado el jugador que ha jugado en el ultimo turno
# @Partida_id
# @return jugador(username)
def calcular_sig_jugador(Partida_id):

    Partdia = Partida.objects.filter(Partida_id).first() or None
    if Partida == None:
        return 'Error, no existe partida'
    else:
        lista_j = Partida.orden_jugadores
        turno = Partida.turno_actual
        Partida.turno_actual = (turno + 1) % 6
        Partida.save()

        return lista_j[turno % 6]