from trivial_api.models import *
from trivial_api.serializers import *

#Token
from rest_framework.authtoken.models import Token
    
def lista_usuarios_sala(room_name):
    usuarios = UsuariosSala.objects.filter(nombre_sala=room_name).values("username")
    lista_usuarios=""
    for i in usuarios:
        lista_usuarios = lista_usuarios + str(i['username'] + ',')
    lista_usuarios = lista_usuarios[:-1]

    return lista_usuarios
    