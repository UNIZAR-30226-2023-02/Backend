from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions,generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import re
from datetime import datetime

#Token
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


def extract_token(token):
    return token[6:]

#Comprobamos que el token pertenece al usuario que realmente quiere acceder
def isAuthorized(token,username):
    user_id = get_object_or_404(Usuario, username=username).id
    token_user_id = Token.objects.get(key=token).user_id
    if(user_id == token_user_id):
        return True
    return False

def get_username_and_token(request):
    if request.method == 'POST':
        username = request.data.get('username')
    elif request.method == 'GET':
        username = request.GET.get('username')
    token= request.headers['Authorization']
    return username,extract_token(token)

def get_token(request):
    token= request.headers['Authorization']
    return extract_token(token)


class UsuarioLogin(APIView):
    def post(self, request):
        any_error = 0
        dict_response = {
            'OK':"",
            'token':"",
            'error_username': "",
            'error_password': "",
        }
        # Retrieve the credentials from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Comprobacion de errores
        # Busca si existe el usuario, si no existe guarda None en user
        user = Usuario.objects.filter(username=username).first() or None

        if user == None:
            dict_response['error_username'] = "Usuario invalido"
            any_error = 1
        else:
            if not user.check_password(password):
                dict_response['error_password'] = "Contraseña invalida"
                any_error = 1

        if any_error == 0:
            #Se crea un token asociado al usuario
            token,_ = Token.objects.get_or_create(user=user)
            dict_response['token'] = token.key
            print(token.key)
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        
        return Response(dict_response)


class UsuarioRegistrar(APIView):
    def post(self, request):
        any_error = 0
        # Diccionario con lo que devolvera en la peticion
        dict_response = {
            'OK':"",
            'error_username': "",
            'error_password': "",
            'error_confirm_password': "",
            'error_fecha_nac': "",
            'error_correo': "",
            'error_telefono':"",
        }
        username = request.data.get('username')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        fecha_nac = request.data.get('fecha_nac')
        correo = request.data.get('correo')
        telefono = request.data.get('telefono')

        # Check usuario
        if not username:
            dict_response['error_username'] = "El usuario no puede ser vacio"
            any_error = 1
        elif Usuario.objects.filter(username=username).exists():
            # Comprobamos que no exista el usuario
            dict_response['error_username'] = "El usuario ya existe"
            any_error = 1

        # Check contraseña
        if len(password) < 8:
            dict_response['error_password'] = "Contraseña inferior a 8 carácteres"
            any_error = 1
        elif password != confirm_password:
            dict_response['error_password'] = "Contraseñas diferentes"
            dict_response['error_confirm_password'] = "Contraseñas diferentes"
            any_error = 1
        
        # # Check correo
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
        if not correo:
            dict_response['error_correo'] = "Correo no puede estar vacio"
            any_error = 1
        elif not re.search(regex,correo):
            dict_response['error_correo'] = "Correo no valido"
            any_error = 1
        elif Usuario.objects.filter(correo=correo).exists():
            dict_response['error_correo'] = "El correo ya esta en uso"
            any_error = 1

        # Check telefono
        if not telefono:
            dict_response['error_telefono'] = "El telefono no puede estar vacio"
            any_error = 1
        elif len(telefono) < 9:
            dict_response['error_telefono'] = "Telefono inferior a 9 numeros"
            any_error = 1
            
        # Check fecha nacimiento
        try:
            datetime.strptime(fecha_nac, '%Y-%m-%d')
        except ValueError:
            dict_response['error_fecha_nac'] = "Formato fecha nacimiento invalido(YY-MM-DD)"

        # Si tenemos errores
        if any_error ==0:
            # Creamos el registro en la base de datos
            user = Usuario.objects.create(username=username, correo=correo,telefono = telefono,fecha_nac=fecha_nac,password=password)
            user.set_password(password)
            user.save()
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        return Response(dict_response)

class UsuarioDatos(APIView):
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]

    def get(self, request):
        #Con esto comprobamos si el usuario tiene acceso a la informacion
        username, token = get_username_and_token(request)
        if(not isAuthorized(token,username)):
            return Response({"detail":"No tienes acceso a la informacion"}, status=401)
        
        any_error = 0
        dict_response = {
            'OK':"",
            'username':"",
            'correo': "",
            'fecha_nac': "",
            'monedas': "",
            'amigos':[],
        }

        if Usuario.objects.filter(username=username).exists():
            user = Usuario.objects.get(username=username)
            amigos = Amigos.objects.filter(username=username)
            dict_response['username'] = user.username
            dict_response['correo'] = user.correo
            dict_response['fecha_nac'] = user.fecha_nac
            dict_response['monedas'] = user.monedas    
            for amigo in amigos:
                dict_response['amigos'].append(str(amigo.amigo))      
            print(dict_response) 
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        return Response(dict_response)


class UsuarioAddAmigo(APIView):
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    def post(self, request):
        #Con esto comprobamos si el usuario tiene acceso a la informacion
        username, token = get_username_and_token(request)
        if(not isAuthorized(token,username)):
            return Response({"detail":"No tienes acceso a la informacion"}, status=401)
        
        any_error = 0
        dict_response = {
            'OK':"",
            'error':""
        }

        amigo = request.data.get('amigo')

        if not Usuario.objects.filter(username=username).exists():
            any_error = 1
            dict_response['error'] = "El usuario no existe"

        if Amigos.objects.filter(username=username,amigo=amigo).exists():
            any_error = 1
            dict_response['error'] = "Ya tienes el amigo agregado"

        if not Usuario.objects.filter(username=amigo).exists():
            any_error =1
            dict_response['error'] = "El usuario que intentas agregar no existe"
                
        if username == amigo:
            any_error =1
            dict_response['error'] = "El usuario no puede ser amigo de si mismo"

        if any_error ==0:
            usuario_instance = get_object_or_404(Usuario, username=username)
            amigo_instance = get_object_or_404(Usuario, username=amigo)
            amigo_db = Amigos.objects.create(username_id=usuario_instance,amigo_id=amigo_instance)
            amigo_db.save()
            dict_response['OK'] = "True"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)
    

class SalaCrear(APIView):
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    def post(self, request):
        any_error = 0
        dict_response = {
            'OK':"",
            'error_nombre_sala':"",
            'error_tipo_sala':"",
            'error_tipo_partida':"",
            'error_n_jugadores':"",
            'error_tiempo_respuesta':"",
        }
        token = get_token(request)
        #Obtener el nombre de usuario dado el token
        username = Token.objects.get(key=token).user

        nombre_sala = request.data.get('nombre_sala')
        tiempo_respuesta = request.data.get('tiempo_respuesta')
        password_sala = request.data.get('password_sala')
        n_jugadores = request.data.get('n_jugadores')
        tipo_partida = request.data.get('tipo_partida')
        
        if not password_sala:
            tipo_sala = "Publico"
        else:
            tipo_sala = "Privado"

        #Check nombre_sala
        if Sala.objects.filter(nombre_sala=nombre_sala).exists():
            any_error = 1
            dict_response['error_nombre_sala'] = "La sala ya existe, selecciona otro nombre"
        
        #Check tipo_sala
        if tipo_sala not in dict(Sala.SALA_CHOICES):
            any_error = 1
            dict_response['error_tipo_sala'] = "Solo son validos: Publico,Privado "

        #Check tipo_partida
        if tipo_partida not in dict(Sala.PARTIDA_CHOICES):
            any_error = 1
            dict_response['error_tipo_partida'] = "Solo son validos: Clasico,Equipo,Tematico"

        #Check n_jugadores
        if(int(n_jugadores) <2 or int(n_jugadores) >6):
            any_error = 1
            dict_response['error_n_jugadores'] = "El numero de jugadores tiene que ser entre 2 y 6"

        #Check tiempo_respuesta
        if(int(tiempo_respuesta) <10 or int(tiempo_respuesta) >50):
            any_error = 1
            dict_response['error_tiempo_respuesta'] = "Tiempo de respuesta invalido"

        if any_error ==0:
            usuario_instance = get_object_or_404(Usuario, username=username)
            # Creamos la sala
            sala = Sala.objects.create(nombre_sala=nombre_sala,creador=usuario_instance,tiempo_respuesta=tiempo_respuesta
                                       ,n_jugadores=n_jugadores,password_sala=password_sala,tipo_partida=tipo_partida,tipo_sala=tipo_sala)
            sala.set_password(password_sala)
            sala.save()
            sala_usuario = UsuariosSala.objects.create(nombre_sala=sala,username=usuario_instance,equipo=1)
            sala_usuario.save()
            dict_response['OK'] = "True"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)


class SalaUnirse(APIView):
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    def post(self, request):
        any_error = 0
        dict_response = {
            'OK':"",
            'error_sala':"",
        }
        token = get_token(request)
        #Obtener el nombre de usuario dado el token
        username = Token.objects.get(key=token).user
        nombre_sala = request.data.get('nombre_sala')
        sala = Sala.objects.filter(nombre_sala=nombre_sala).first() or None

        #Check if sala exists
        if sala:
            jugadores_en_partida =  UsuariosSala.objects.filter(nombre_sala=nombre_sala).count()
            if(jugadores_en_partida > sala.n_jugadores):
                any_error = 1
                dict_response['error_sala'] = "La sala esta llena, no puedes unirte"
            usuario_sala = UsuariosSala.objects.filter(nombre_sala=nombre_sala,username=username).first() or None
            if(usuario_sala):
                any_error = 1
                dict_response['error_sala'] = "Ya perteneces a esta sala, no puedes unirte"
        else:
            any_error = 1
            dict_response['error_sala'] = "La sala no existe"
            
        if any_error ==0:
            sala_usuario = UsuariosSala.objects.create(nombre_sala=sala,username=username,equipo=1)
            sala_usuario.save()
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        return Response(dict_response)


class SalaLista(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = get_token(request)
        username = Token.objects.get(key=token).user

        salas = Sala.objects.all()
        serializer = SalaSerializer(salas, many=True)
        return Response(serializer.data)


#Lista los jugadores y el equipo al que pertencen en la sala especificada
class SalaListaJugadoresSala(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = get_token(request)
        username = Token.objects.get(key=token).user
        nombre_sala = request.data.get('nombre_sala')
        sala = Sala.objects.filter(nombre_sala=nombre_sala).first() or None
        if(sala):
            # Filter Sala objects based on nombre
            usuarios = UsuariosSala.objects.filter(nombre_sala=sala)
            # Get list of usernames
            usernames = [{'username': str(usuario.username),'equipo': str(usuario.equipo)} for usuario in usuarios]
        else:
            usernames = []
        return Response(usernames)





# class SalaEliminar(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         #Con esto comprobamos si el usuario tiene acceso a la informacion
#         username, token = get_username_and_token(request)
#         if(not isAuthorized(token,username)):
#             return Response({"detail":"No tienes acceso a la informacion"}, status=401)
        



# class UnirseSala(APIView):
#     #Necesita la autenticazion
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         #Con esto comprobamos si el usuario tiene acceso a la informacion
#         username, token = get_username_and_token(request)
#         if(not isAuthorized(token,username)):
#             return Response({"detail":"No tienes acceso a la informacion"}, status=401)
        
#         if not sala.check_password(password):
#                 dict_response['error_password'] = "Contraseña invalida"
#                 any_error = 1