#
#Fichero de funciones axuiliares para el transcurso de una partida
#

import json
from trivial_api.models import *
from partida.models import *
from sala.models import *
import random




def calcular_jugadores(Partida_id):
    game = Partida.objects.filter(id = Partida_id).first() or None
    jugadores = game.orden_jugadores.split(',')
    return len(jugadores)



# Función que devulve un valor aleatorio del 1-6 simulando la tirada de un dado
# @return string [1-6] 
def tirar_dado():
    return str(random.randint(1,6))


# Funcion que devuleve a que casillas puede llegar dados
#   una casilla y un numero de dado
# @param string(tirada [1-6])
# @param string(jugdor username)
# @param string(Partida_id numero)
# @return 
def calcular_siguiente_movimiento(tirada, jugador, Partida_id):

    Casillas = ""
    posicion = Juega.objects.filter(username_id = jugador, id_partida = Partida_id).values('posicion').first()
    for i in Tablero.objects.filter(casilla_actual=posicion['posicion'], tirada_dado=tirada).values('casilla_nueva'):
        Casillas =  Casillas + str(i['casilla_nueva']) + ","
    
    Casillas = Casillas[:-1]
    return Casillas


# Elige una pregunta al hacer dependiendo de la casilla que se le pase
# Depende de la casilla sera de una tematica u otra
# @param casilla([1-72])
# @param string(jugdor username)
# @param string(Partida_id numero)
# @return vector(pregunta, r1, r2, r3, r4, rc)
def elegir_pregunta(casilla, jugador, Partida_id, tematica = None):

    mov_posicion = Juega.objects.filter(username_id = jugador, id_partida = Partida_id).first()
    if mov_posicion == None:
        return None
    
    mov_posicion.posicion = casilla
    mov_posicion.save()

    if casilla == "72":
        listaTematicas = ['Historia','Entretenimiento','Ciencia','Geografia','Arte','Deportes']
        inf_casilla = {}
        inf_casilla['quesito'] = "false"
        inf_casilla['tematica'] = listaTematicas[random.randint(0, len(listaTematicas) - 1)]
    else:
        inf_casilla = Casilla_Tematica.objects.filter(casilla = casilla).values('tematica', 'quesito').first()

    if tematica:
        inf_casilla['tematica'] = tematica
    

    print("La tematica elegida es: " + inf_casilla['tematica'])
    
    if inf_casilla['tematica'] == 'Dados':
        pregunta_devolver = {'enunciado':""}
        pregunta_devolver['enunciado'] = 'repetir'
        return pregunta_devolver
    
    all_preguntas = Pregunta.objects.values('enunciado', 'r1', 'r2', 'r3', 'r4', 'rc').filter(categoria = inf_casilla['tematica'])
    pregunta_devolver = all_preguntas[random.randint(0,len(all_preguntas) - 1)]
    #pregunta_devolver = [enunciado, r1, r2, r3, r4, rc]

    respuestas = []
    for i in ['r1','r2','r3','r4']:
        respuestas.append(pregunta_devolver[i])
    random.shuffle(respuestas)
    rc = respuestas.index(pregunta_devolver['r1'])

    j = 0
    for i in ['r1','r2','r3','r4']:
        pregunta_devolver[i] = respuestas[j]
        j = j + 1
    pregunta_devolver['rc'] = rc+1


    pregunta_devolver['tematica'] = inf_casilla['tematica']

    pregunta_devolver['quesito'] = inf_casilla['quesito']


    

    return pregunta_devolver


# Elige una pregunta al hacer dependiendo de la casilla que se le pase
# Depende de la casilla sera de una tematica u otra
# @param casilla([1-72])
# @param string(jugdor username)
# @param string(Partida_id numero)
# @return vector(pregunta, r1, r2, r3, r4, rc)
def elegir_pregunta(casilla, jugador, Partida_id):

    mov_posicion = Juega.objects.filter(username_id = jugador, id_partida = Partida_id).first()
    if mov_posicion == None:
        return None
    
    mov_posicion.posicion = casilla
    mov_posicion.save()

    if casilla == "72":
        listaTematicas = ['Historia','Entretenimiento','Ciencia','Geografia','Arte','Deportes']
        inf_casilla = {}
        inf_casilla['quesito'] = "false"
        inf_casilla['tematica'] = listaTematicas[random.randint(0, len(listaTematicas) - 1)]
    else:
        inf_casilla = Casilla_Tematica.objects.filter(casilla = casilla).values('tematica', 'quesito').first()

    print("La tematica elegida es: " + inf_casilla['tematica'])
    
    if inf_casilla['tematica'] == 'Dados':
        pregunta_devolver = {'enunciado':""}
        pregunta_devolver['enunciado'] = 'repetir'
        return pregunta_devolver
    
    all_preguntas = Pregunta.objects.values('enunciado', 'r1', 'r2', 'r3', 'r4', 'rc').filter(categoria = inf_casilla['tematica'])
    pregunta_devolver = all_preguntas[random.randint(0,len(all_preguntas) - 1)]
    #pregunta_devolver = [enunciado, r1, r2, r3, r4, rc]

    respuestas = []
    for i in ['r1','r2','r3','r4']:
        respuestas.append(pregunta_devolver[i])
    random.shuffle(respuestas)
    rc = respuestas.index(pregunta_devolver['r1'])

    j = 0
    for i in ['r1','r2','r3','r4']:
        pregunta_devolver[i] = respuestas[j]
        j = j + 1
    pregunta_devolver['rc'] = rc+1


    pregunta_devolver['tematica'] = inf_casilla['tematica']

    pregunta_devolver['quesito'] = inf_casilla['quesito']


    

    return pregunta_devolver

# Marca el queso de la categoria que sea para el judaro dado y comprobar si es el ultimo queso
# @param queso([historia, arte, ciencia, geografia, entretenimiento, deportes])
# @param jugador(usernema)
# @Partida_id 
# @return True si el jugador ha conseguido todos los quesos
def marcar_queso(queso, jugador, Partida_id):
    
    juega = Juega.objects.filter(username_id = jugador, id_partida = Partida_id).first()
    
    
    if Partida == None:
        return False
    else:
        if queso == 'Historia':
            if juega.q_historia == False:
                juega.q_historia = True
        elif queso == 'Arte':
            if juega.q_arte == False:
                juega.q_arte = True

        elif queso == 'Deportes':
            if juega.q_deporte == False:
                juega.q_deporte = True

        elif queso == 'Entretenimiento':
            if juega.q_entretenimiento == False:
                juega.q_entretenimiento = True

        elif queso == 'Ciencia':
            if juega.q_ciencia == False:
                juega.q_ciencia = True

        elif queso == 'Geografia': 
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

    game = Partida.objects.filter(id = Partida_id).first() or None

    if game == None:
        return 'Error, no existe partida'
    else: 
        #Pepe,Juan,P
        #Juan, P ,Pepe
        lista_j = game.orden_jugadores
        
        lista_j = lista_j.split(',')
        primer_elemento = lista_j.pop(0)
        lista_j.append(primer_elemento)
        segundo_elemento = lista_j.pop(0)
        lista_j.insert(0, segundo_elemento)
        
        
        game.orden_jugadores = ",".join(lista_j)
        # turno = game.turno_actual
        # game.turno_actual = str((int(turno) + 1) % calcular_jugadores(Partida_id))
        game.save()

        return lista_j[0]
    
    
# Devuelve el jugador que tiene el turno
def jugador_con_turno(Partida_id):
    game = Partida.objects.filter(id = Partida_id).first() or None
    if game == None:
        return 'Error, no existe partida'
    else:
        lista_j = game.orden_jugadores
        lista_j = lista_j.split(',')
        return lista_j[int(game.turno_actual)]

    
# Recupera en una lista todos los quesitos que tiene un jugador en la partida
# @juega -> Necesita ser la instancia del modelo, que se obtiene con el id_partida y el usuario
def obtener_quesitos_jugador(juega):
    lista_quesitos = []
    if juega.q_historia:
        lista_quesitos.append("Historia")
    if juega.q_arte:
        lista_quesitos.append("Arte")
    if juega.q_deporte:
        lista_quesitos.append("Deporte")
    if juega.q_ciencia:
        lista_quesitos.append("Ciencia")
    if juega.q_entretenimiento:
        lista_quesitos.append("Entretenimiento")
    if juega.q_geografia:
        lista_quesitos.append("Geografía")
    return lista_quesitos
    


# Funcion que obtiene los datos de todos los jugadores de la partida
# @jugadores -> el orden de los jugadores en partida
def cargar_datos_partida(self):
    mensaje_inicio = {
        'OK':"",
        'jugadores':[],
        'tiempo_pregunta': "",
        'tiempo_elegir_casilla': "",
        'error': "",
    }
    partida = Partida.objects.filter(id=self.game_name).first() or None

    mensaje_inicio['OK'] = "true"
    mensaje_inicio['tiempo_pregunta'] = str(partida.tiempo_respuesta)
    mensaje_inicio['tiempo_elegir_casilla'] = "5"
    jugadores = partida.orden_jugadores.split(',')
    for i, jugador in enumerate(jugadores):
        informacion_jugador = {'jugador':'','posicion':'','quesitos':[],'turno':'','ficha':'','tablero':'','activo':''}
        user = Usuario.objects.filter(username=jugador).first() or None
        juega = Juega.objects.filter(username=user,id_partida=partida).first() or None

        informacion_jugador["quesitos"] = obtener_quesitos_jugador(juega)
        informacion_jugador["jugador"] = str(juega.username)
        informacion_jugador["posicion"] = str(juega.posicion)
        informacion_jugador["turno"] = str(i)
        informacion_jugador["ficha"] = str(juega.image)
        informacion_jugador["tablero"] = str(user.image_tablero)
        informacion_jugador["activo"] = str(juega.activo)
        mensaje_inicio["jugadores"].append(informacion_jugador)
    return mensaje_inicio


def actualizar_estadisticas(user,tematica,bien,quesito):
    stats = Estadisticas.objects.filter(username=user).first() or None
    if(bien):
        if(tematica == "Historia"):
            stats.historia_bien +=1
        elif(tematica == "Arte"):
            stats.arte_y_literatura_bien +=1
        elif(tematica == "Deportes"):
             stats.deportes_bien +=1
        elif(tematica == "Entretenimiento"):
            stats.entretenimiento_bien +=1
        elif(tematica == "Ciencia"):
            stats.ciencias_bien +=1
        elif(tematica == "Geografia"):
            stats.geografia_bien +=1
    else:
        if(tematica == "Historia"):
            stats.historia_mal +=1
        elif(tematica == "Arte"):
            stats.arte_y_literatura_mal +=1
        elif(tematica == "Deportes"):
             stats.deportes_mal +=1
        elif(tematica == "Entretenimiento"):
            stats.entretenimiento_mal +=1
        elif(tematica == "Ciencia"):
            stats.ciencias_mal +=1
        elif(tematica == "Geografia"):
            stats.geografia_mal +=1

    if(quesito):
        stats.quesitos +=1

    stats.save()



def actualizar_estadisticas_partida(ganador, jugadores):
    
    
    for i in jugadores.split(','):
        
        stats = Estadisticas.objects.filter(username=i).first() or None
        
        if ganador == i:
            stats.partidas_ganadas += 1
        else:
            stats.partidas_perdidas += 1

        stats.save()



