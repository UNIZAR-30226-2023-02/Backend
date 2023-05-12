from .models import *
from sala.models import *
from partida.models import *
from .serializers import *

#Token
from rest_framework.authtoken.models import Token

# Auxiliares
import re
from datetime import datetime


#Funcion para comprobar si el caracter introducido es ascii
def isascii(s):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(s) == len(s.encode())


# Funcion que devuelve TRUE si no hay ningun error, False en caso contario
def all_errors_empty(dict_response):
    for key in dict_response.keys():
        if key.startswith('error') and dict_response[key]:
            return False
    return True



def validate_username_register(username):
    mensaje_error = ""
    # Check usuario
    if not isascii(username):
        mensaje_error = "Usuario con caracteres no permitidos"
    elif not username:
        mensaje_error = "El usuario no puede ser vacio"
    elif len(username) < 1 or len(username) > 20:
        mensaje_error = "El usuario no tiene la longitud correcta(1-20)"
    elif Usuario.objects.filter(username=username).exists():
        mensaje_error = "El usuario ya existe"
    return mensaje_error

def validate_password_register(password,confirm_password):
    mensaje_error1 = ""
    mensaje_error2 = ""
    if not isascii(password):
        mensaje_error1 = "Contraseña con caracteres no permitidos"
    elif len(password) < 8:
        mensaje_error1 = "Contraseña inferior a 8 carácteres"
    elif password != confirm_password: # Hacer que comprueben que es la misma en el front-end
        mensaje_error1 = "Contraseñas diferentes"
        mensaje_error2 = "Contraseñas diferentes"
    return mensaje_error1, mensaje_error2


def validate_correo_register(correo):
    mensaje_error = ""
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
    if not correo:
        mensaje_error = "El correo no puede estar vacio"
    elif not re.search(regex,correo):
        mensaje_error = "Correo no valido"
    elif Usuario.objects.filter(correo=correo).exists():
        mensaje_error = "El correo ya esta en uso"
    return mensaje_error

def validate_telefono(telefono):
    mensaje_error = ""
    # Check telefono
    if not telefono:
        mensaje_error = "El telefono no puede estar vacio"
    elif not str(telefono).isnumeric():
        mensaje_error = "Telefono no numerico"
    elif len(str(telefono)) < 9 :
        mensaje_error = "Telefono inferior a 9 numeros"
    return mensaje_error

def validate_fecha_nac(fecha_nac):
    mensaje_error = ""
    try:
        datetime.strptime(fecha_nac, '%Y-%m-%d')
    except ValueError:
        mensaje_error = "Formato fecha nacimiento invalido(YYYY-MM-DD)"
    return mensaje_error


def validate_correo_cambiar_datos(correo,user_correo,username):
    mensaje_error = ""
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
    if not correo:
        mensaje_error = "El correo no puede estar vacio"
    elif not re.search(regex,correo):
        mensaje_error = "Correo no valido"
    elif user_correo and user_correo.username != username:
        mensaje_error = "El correo ya esta en uso"
    return mensaje_error


def existe_usuario(username):
    return Usuario.objects.filter(username=username).exists()
            
def es_amigo(username,amigo_username):
    return Amigos.objects.filter(user1=username,user2=amigo_username).exists()

def validate_sala_crear(nombre_sala):
    mensaje_error = ""
    if Sala.objects.filter(nombre_sala=nombre_sala).exists():
        mensaje_error = "La sala ya existe, selecciona otro nombre"
    elif not nombre_sala.isascii():
        mensaje_error = "La sala tiene caracteres no permitidos"
    return mensaje_error


# Comprobamos si el usuario tiene una partida no terminada, que no pueda entrar ni a una sala ni partida.

def rechazar_reconexion(user):
    for i in Juega.objects.filter(username=user).values('id_partida'):
        partida = Partida.objects.filter(id=int(i['id_partida']),terminada=False).first or None
        if(partida):
            return True
        
    return False



#######################
#   FUNCIONES TOKEN   #
#######################

#Parseamos el token para solo obtener la parte que nos interesa.
def extract_token(token):
    return token[6:]

#Obtenemos el usuario y el token de la peticion
def get_username_and_token(request):
    token= request.headers['Authorization']
    username = None
    try:
        token = extract_token(token)
        print(token)
        user_token = Token.objects.filter(key=token).first() or None
        if(user_token):
            user_id = user_token.user_id
        print(user_id)
        user = Usuario.objects.filter(username=user_id).first() or None
        print(user)
        username = user.username
    except:
        print("No se ha podido extraer el token y el usuario")
    return username,token


#Obtenemos el nombre de usuario dado el token
def get_username_by_token(request):

    token= request.headers.get('Authorization')
    username = None
    usuario = Token.objects.filter(key=token).first() or None
    print(usuario)
    if(usuario):
        username = usuario.user_id
    return username
