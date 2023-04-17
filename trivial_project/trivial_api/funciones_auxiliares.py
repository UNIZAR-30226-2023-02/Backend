#Token
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
import re
from datetime import datetime
from .models import *
from .serializers import *

#Funcion para comprobar si el caracter introducido es ascii
def isascii(s):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(s) == len(s.encode())

#Parseamos el token para solo obtener la parte que nos interesa.
def extract_token(token):
    return token[6:]


def get_username_by_id(user_id):
    print(user_id)
    user = Usuario.objects.filter(username=user_id).first() or None
    if(user):
        return user.username
    else:
        return None

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

#Obtenemos el usuario y el token de la peticion
def get_userID_and_token(request):
    token= request.headers['Authorization']
    user_id = None
    try:
        token = extract_token(token)
        user_token = Token.objects.filter(key=token).first() or None
        if(user_token):
            user_id = user_token.user_id
            print("El usuario id es: ",user_id)
    except:
        print("No se ha podido extraer el token y el usuario")
    return user_id,token

#Obtenemos el token de la peticion
def get_token(request):
    token= request.headers['Authorization']
    return extract_token(token)

#Obtenemos el nombre de usuario dado el token
def get_username_by_token(token):
    username = None
    usuario = Token.objects.filter(key=token).first() or None
    if(usuario):
        user = Usuario.objects.filter(username=usuario.user_id).first() or None
        username = user.username
    return username

def get_userID_by_username(username):
    user_id = None
    user = Usuario.objects.filter(username=username).first() or None
    if(user):
        user_id = user.username
    else:
        user_id = None
    return user_id