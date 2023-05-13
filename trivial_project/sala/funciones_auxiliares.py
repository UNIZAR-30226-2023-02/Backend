from trivial_api.models import *
from trivial_api.serializers import *
import random

#Token
from rest_framework.authtoken.models import Token
    
def lista_usuarios_sala(room_name):
    usuarios = UsuariosSala.objects.filter(nombre_sala=room_name).values("username")
    lista_usuarios=""

    for i in usuarios:
        lista_usuarios = lista_usuarios + str(i['username'] + ',')
    lista_usuarios = lista_usuarios[:-1]

    return lista_usuarios

def usuarios_orden_aleatorio(room_name, tipo):
    usuarios = UsuariosSala.objects.filter(nombre_sala=room_name).values("username")
    # usuarios = []
    # for i in usuarios_dic:
    #     usuarios.append(str(i['username']))
    # lista_usuarios=""
    usuarios = list(usuarios)
    # Generamos el orden aleatorio
    random.shuffle(usuarios)
    if tipo == "Equipo":
        lista_usuarios = ""
        while (len(usuarios) > 0):
            lista_usuarios = lista_usuarios + ",".join(usuarios[0:2]) + ";"
            usuarios = usuarios[2:]
        lista_usuarios = lista_usuarios[:-1]
    else:
        for i in usuarios:
            lista_usuarios = lista_usuarios + str(i['username'] + ',')
        lista_usuarios = lista_usuarios[:-1]

    return lista_usuarios




def calcular_jugadores(Partida_id):

    game = Partida.objects.filter(id = Partida_id).first() or None
    jugadores = game.orden_jugadores.split(',')
    return len(jugadores)


def orden_inicio_jugadores(Partida_id):
    game = Partida.objects.filter(id = Partida_id).first() or None

    if game != None:
        jugadores = game.orden_jugadores.split(',')
        random.shuffle(jugadores)
        return jugadores
        
    else:
        return game.orden_jugadores.split(',')
    
# Función crea en la base de datos una instancia del jugador y la partida
# @param string(Partida_id numero)
# @return true si la ha podido crear false en caso contrario 
def generar_jugadores(game):
    jugadores = game.orden_jugadores.split(',')

    for i in jugadores:
        user = Usuario.objects.filter(username = i).first()
        user_partida = Juega.objects.create(username_id = user, id_partida = game)
        user_partida.save()