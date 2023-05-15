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
    if game.tipo == "Equipo":
        jugadores = []
        equipos = game.orden_jugadores.split(';')
        for e in equipos:
            jugadores = jugadores + e.split(',')
    else:
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
def elegir_pregunta(casilla, jugador, Partida_id, tematica = False):
    mov_posicion = Juega.objects.filter(username_id = jugador, id_partida = Partida_id).first()
    if mov_posicion == None:
        return None
    
    mov_posicion.posicion = casilla
    mov_posicion.save()

    if str(casilla) == "72":
        listaTematicas = ['Historia','Entretenimiento','Ciencia','Geografia','Arte','Deportes']
        inf_casilla = {}
        inf_casilla['quesito'] = "false"
        inf_casilla['tematica'] = listaTematicas[random.randint(0, (len(listaTematicas) - 1))]
    else:
        inf_casilla = Casilla_Tematica.objects.filter(casilla = casilla).values('tematica', 'quesito').first()

    if tematica:
        inf_casilla['tematica'] = tematica
        inf_tematica_quesito = Casilla_Tematica_Tematico.objects.filter(casilla = casilla).values('tematica', 'quesito').first()
        if inf_tematica_quesito['tematica'] == 'Dados':
            pregunta_devolver = {'enunciado':""}
            pregunta_devolver['enunciado'] = 'repetir'
            return pregunta_devolver
    else:
        if inf_casilla['tematica'] == 'Dados':
            pregunta_devolver = {'enunciado':""}
            pregunta_devolver['enunciado'] = 'repetir'
            return pregunta_devolver


    print("La tematica elegida es: " + inf_casilla['tematica'])

    all_preguntas = Pregunta.objects.values('enunciado', 'r1', 'r2', 'r3', 'r4', 'rc').filter(categoria = inf_casilla['tematica'])
    pregunta_devolver = all_preguntas[random.randint(0,len(all_preguntas) - 1)]

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

    if tematica:
        pregunta_devolver['tematica'] = inf_tematica_quesito['tematica']

        pregunta_devolver['quesito'] = inf_tematica_quesito['quesito']
    else:
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
def calcular_sig_jugador(Partida_id, equipos = None):

    game = Partida.objects.filter(id = Partida_id).first() or None

    if game == None:
        return 'Error, no existe partida'
    else: 
        #Pepe,Juan,P
        #Juan, P ,Pepe
        # Contar el numero de jugadores activos
        if equipos == True:
            print("Cambiando turno al siguiente equipo")

            lista_equipos = game.orden_jugadores.split(';') #Cambiamos al siguiente equipo
            primer_elemento = lista_equipos.pop(0)
            lista_equipos.append(primer_elemento)

            lista_j = lista_equipos[0].split(',') # Cambiamos al siguiente jugador
            primer_elemento = lista_j.pop(0)
            lista_j.append(primer_elemento)

            activo = False
            i = 0
            
            while (not activo):
                jugador = Juega.objects.filter(username=lista_j[0], id_partida = Partida_id).first() or None
                if (jugador and jugador.activo):
                    activo  = True
                else:
                    primer_elemento = lista_j.pop(0)
                    lista_j.append(primer_elemento)
                    i+= 1

                if i == 10:
                    return None
            
            lista_equipos[0] = ",".join(lista_j)

            game.orden_jugadores = ";".join(lista_equipos)
            game.save()

        else:
            lista_j = game.orden_jugadores
            
            lista_j = lista_j.split(',')

            primer_elemento = lista_j.pop(0)
            lista_j.append(primer_elemento)

            activo = False
            i = 0
            
            while (not activo):
                jugador = Juega.objects.filter(username=lista_j[0], id_partida = Partida_id).first() or None
                if (jugador and jugador.activo):
                    activo  = True
                else:
                    primer_elemento = lista_j.pop(0)
                    lista_j.append(primer_elemento)
                    i+= 1

                if i == 10:
                    return None
            
            
            game.orden_jugadores = ",".join(lista_j)
            game.save()

        return lista_j[0]
    
# Calcula el siguente jugador del equipo a jugar dado el jugador que ha jugado en el ultimo turno
# @Partida_id
# @return jugador(username)
def calcular_sig_jugador_equipo(Partida_id):

    game = Partida.objects.filter(id = Partida_id).first() or None

    if game == None:
        return 'Error, no existe partida'
    else: 
        lista_equipos = game.orden_jugadores
        
        lista_equipos = lista_equipos.split(';')

        lista_j = lista_equipos[0].split(',')

        primer_elemento = lista_j.pop(0)
        lista_j.append(primer_elemento)

        activo = False
        i = 0
        
        while (not activo):
            jugador = Juega.objects.filter(username=lista_j[0], id_partida = Partida_id).first() or None
            if (jugador and jugador.activo):
                activo  = True
            else:
                primer_elemento = lista_j.pop(0)
                lista_j.append(primer_elemento)
                i+= 1

            if i == 10:
                return None
        
        lista_equipos[0] = ",".join(lista_j)
        
        game.orden_jugadores = ";".join(lista_equipos)
        game.save()

        return lista_j[0]
    
def obtener_jugadores_equipo(Partida_id):
    game = Partida.objects.filter(id = Partida_id).first() or None

    if game == None:
        return 'Error, no existe partida'
    else: 
        lista_equipos = game.orden_jugadores
        
        lista_equipos = lista_equipos.split(';')

        lista_j = lista_equipos[0].split(',')
        return lista_j[0],lista_j[1] # Devuelve los dos jugadores del equipo
       

    
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
        lista_quesitos.append("Deportes")
    if juega.q_ciencia:
        lista_quesitos.append("Ciencia")
    if juega.q_entretenimiento:
        lista_quesitos.append("Entretenimiento")
    if juega.q_geografia:
        lista_quesitos.append("Geografia")
    return lista_quesitos
    


# Funcion que obtiene los datos de todos los jugadores de la partida
# @jugadores -> el orden de los jugadores en partida
# @inicio -> si es al principio de la partida =True, en caso contrario false
def cargar_datos_partida(self,inicio):
    mensaje_inicio = {
        'OK':"",
        'jugadores':[],
        'tiempo_pregunta': "",
        'tematica':"",
        'tiempo_elegir_casilla': "",
        'error': "",
    }
    partida = Partida.objects.filter(id=self.game_name).first() or None

    mensaje_inicio['OK'] = "true"
    mensaje_inicio['tiempo_pregunta'] = str(partida.tiempo_respuesta)
    mensaje_inicio['tiempo_elegir_casilla'] = "10"
    mensaje_inicio['tematica'] = str(partida.tematica)

    if partida.tipo == "Equipo":
        equipos = partida.orden_jugadores_inicial.split(';')
        print("Cargando modo equipos: " + str(equipos))
        for e,equipo in enumerate(equipos):
            jugadores = equipo.split(',')    
            for i,jugador in enumerate(jugadores):
                informacion_jugador = {'jugador':'','posicion':'','quesitos':[],'turno':'','ficha':'','tablero':'','activo':'','equipo':''}
                user = Usuario.objects.filter(username=jugador).first() or None
                juega = Juega.objects.filter(username=user,id_partida=partida).first() or None
                if(e==0):
                    turno = 1
                else:
                    turno = 0
                informacion_jugador["quesitos"] = obtener_quesitos_jugador(juega)
                informacion_jugador["jugador"] = str(juega.username)
                informacion_jugador["posicion"] = str(juega.posicion)
                informacion_jugador["turno"] = str(turno)
                juega.image = asignar_color_ficha(user.image_ficha,e)
                informacion_jugador["ficha"] = str(juega.image)
                informacion_jugador["tablero"] = str(user.image_tablero)
                informacion_jugador["activo"] = str(juega.activo)
                informacion_jugador["equipo"] = str(e)
                print("Añadiendo al jugador "+ str(jugador) + " al equpo " + str(e))
                mensaje_inicio["jugadores"].append(informacion_jugador)
    else:
        jugadores = partida.orden_jugadores_inicial.split(',')
        
        for i,jugador in enumerate(jugadores):
            informacion_jugador = {'jugador':'','posicion':'','quesitos':[],'turno':'','ficha':'','tablero':'','activo':''}
            user = Usuario.objects.filter(username=jugador).first() or None
            juega = Juega.objects.filter(username=user,id_partida=partida).first() or None
            if(i==0):
                turno = 1
            else:
                turno = 0
            informacion_jugador["quesitos"] = obtener_quesitos_jugador(juega)
            informacion_jugador["jugador"] = str(juega.username)
            informacion_jugador["posicion"] = str(juega.posicion)
            informacion_jugador["turno"] = str(turno)
            juega.image = asignar_color_ficha(user.image_ficha,i)
            informacion_jugador["ficha"] = str(juega.image)
            informacion_jugador["tablero"] = str(user.image_tablero)
            informacion_jugador["activo"] = str(juega.activo)
            mensaje_inicio["jugadores"].append(informacion_jugador)
    return mensaje_inicio


def asignar_color_ficha(url,posicion):
    num_color = {0: "amarillo", 1: "azul", 2: "naranja", 3: "rojo",4:"rosa",5:"verde"}
    color = num_color.get(posicion, "blanco") # si el número no está en el diccionario, se asigna "blanco" por defecto
    color_png = "-" + str(color) + ".png"
    return url.replace(".png", color_png)




def actualizar_estadisticas(user,tematica,bien,quesito):
    stats = Estadisticas.objects.filter(username=user).first() or None
    if(stats):
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
        user = Usuario.objects.filter(username=i).first() or None

        if ganador == i:
            stats.partidas_ganadas += 1
            user.monedas = user.monedas + 5
        else:
            stats.partidas_perdidas += 1
            user.monedas = user.monedas + 2

        user.save()
        stats.save()

def actualizar_estadisticas_partida_equipo(ganador1,ganador2, jugadores):
    for i in jugadores.split(','):
        
        stats = Estadisticas.objects.filter(username=i).first() or None
        user = Usuario.objects.filter(username=i).first() or None

        if ganador1 == i or ganador2 == i:
            stats.partidas_ganadas += 1
            user.monedas = user.monedas + 5
        else:
            stats.partidas_perdidas += 1
            user.monedas = user.monedas + 2

        user.save()
        stats.save()



