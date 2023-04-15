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

from trivial_api.funciones_auxiliares import *

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
            #Se crea un token asociado al usuario, si es la primera vez que inicia.
            #en caso contrario obtiene dicho token
            token,_ = Token.objects.get_or_create(user=user)
            dict_response['token'] = token.key
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
        if not isascii(username):
            dict_response['error_username'] = "Usuario con caracteres no permitidos"
            any_error = 1
        elif not username:
            dict_response['error_username'] = "El usuario no puede ser vacio"
            any_error = 1
        elif len(username) < 1 or len(username) > 20:
            dict_response['error_username'] = "El usuario no tiene la longitud correcta(1-20)"
            any_error = 1
        elif Usuario.objects.filter(username=username).exists():
            # Comprobamos que no exista el usuario
            dict_response['error_username'] = "El usuario ya existe"
            any_error = 1

        # Check contraseña
        if not isascii(password):
            dict_response['error_password'] = "Contraseña con caracteres no permitidos"
            any_error = 1
        elif len(password) < 8:
            dict_response['error_password'] = "Contraseña inferior a 8 carácteres"
            any_error = 1
        elif password != confirm_password: # Hacer que comprueben que es la misma en el front-end
            dict_response['error_password'] = "Contraseñas diferentes"
            dict_response['error_confirm_password'] = "Contraseñas diferentes"
            any_error = 1
        
        # Check correo
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
        if not correo:
            dict_response['error_correo'] = "El correo no puede estar vacio"
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
        elif not telefono.isnumeric():
            dict_response['error_telefono'] = "Telefono no numerico"
            any_error = 1
        elif len(telefono) < 9 :
            dict_response['error_telefono'] = "Telefono inferior a 9 numeros"
            any_error = 1
            
        # Check fecha nacimiento
        try:
            datetime.strptime(fecha_nac, '%Y-%m-%d')
        except ValueError:
            dict_response['error_fecha_nac'] = "Formato fecha nacimiento invalido(YYYY-MM-DD)"

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

    def post(self, request):
        user_id, token = get_userID_and_token(request)
        any_error = 0
        dict_response = {
            'OK':"",
            'username':"",
            'correo': "",
            'fecha_nac': "",
            'monedas': "",
            'amigos':[],
        }

        if Usuario.objects.filter(id=user_id).exists():
            user = Usuario.objects.get(id=user_id)
            amigos = Amigos.objects.filter(user_id=user_id)

            dict_response['username'] = user.username
            dict_response['correo'] = user.correo
            dict_response['fecha_nac'] = user.fecha_nac
            dict_response['monedas'] = user.monedas    
            for amigo in amigos:
                dict_response['amigos'].append(str(amigo.amigo_id))      
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        return Response(dict_response)

class UsuarioCambiarDatos(APIView):
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    def post(self, request):
        #Con esto comprobamos si el usuario tiene acceso a la informacion
        
        any_error = 0
        dict_response = {
            'OK':"",
            'error_username':"",
            'error_correo':"",
            'error_fecha_nac':"",
            'error_telefono':""
        }
        
        user_id, token = get_userID_and_token(request)
        usuario_instancia = Usuario.objects.filter(id=user_id).first() or None
        username = request.data.get('username')
        fecha_nac = request.data.get('fecha_nac')
        correo = request.data.get('correo')
        telefono = request.data.get('telefono')
        
        #Comprobamos si existe el usuario que nos han pasado
        if(usuario_instancia):
            # Check usuario
            if not isascii(username):
                dict_response['error_username'] = "Usuario con caracteres no permitidos"
                any_error = 1
            elif not username:
                dict_response['error_username'] = "El usuario no puede ser vacio"
                any_error = 1
            elif len(username) < 1 or len(username) > 20:
                dict_response['error_username'] = "El usuario no tiene la longitud correcta(1-20)"
                any_error = 1
            elif Usuario.objects.filter(username=username).exists() and usuario_instancia.user_id != user_id:
                # Comprobamos que no exista el usuario, o que el usuario sea distinto al que ya esta
                dict_response['error_username'] = "El usuario ya existe"
                any_error = 1

            # Check correo
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
            if not correo:
                dict_response['error_correo'] = "El correo no puede estar vacio"
                any_error = 1
            elif not re.search(regex,correo):
                dict_response['error_correo'] = "Correo no valido"
                any_error = 1
            elif Usuario.objects.filter(correo=correo).exists() and usuario_instancia.user_id != user_id:
                dict_response['error_correo'] = "El correo ya esta en uso"
                any_error = 1

            # Check telefono
            if not telefono:
                dict_response['error_telefono'] = "El telefono no puede estar vacio"
                any_error = 1
            elif not telefono.isnumeric():
                dict_response['error_telefono'] = "Telefono no numerico"
                any_error = 1
            elif len(telefono) < 9 :
                dict_response['error_telefono'] = "Telefono inferior a 9 numeros"
                any_error = 1
                
            # Check fecha nacimiento
            try:
                datetime.strptime(fecha_nac, '%Y-%m-%d')
            except ValueError:
                dict_response['error_fecha_nac'] = "Formato fecha nacimiento invalido(YYYY-MM-DD)"
        else:
            dict_response['error_username'] = "El token no es valido"
            any_error = 1

        # Si tenemos errores
        if any_error ==0:
            # Creamos el registro en la base de datos
            usuario_instancia.username = username
            usuario_instancia.correo = correo
            usuario_instancia.fecha_nac = fecha_nac
            usuario_instancia.telefono = telefono
            usuario_instancia.save()
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        return Response(dict_response)







class UsuarioAddAmigo(APIView):
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    def post(self, request):
        #Con esto comprobamos si el usuario tiene acceso a la informacion
        user_id, token = get_userID_and_token(request)
        
        any_error = 0
        dict_response = {
            'OK':"",
            'error':""
        }

        amigo = request.data.get('amigo')
        print(amigo)
        amigo_id = get_userID_by_username(amigo)
        print(amigo_id)

        if not Usuario.objects.filter(id=user_id).exists():
            any_error = 1
            dict_response['error'] = "El usuario no existe"

        if Amigos.objects.filter(user_id=user_id,amigo_id=amigo_id).exists():
            any_error = 1
            dict_response['error'] = "Ya tienes el amigo agregado"

        if not Usuario.objects.filter(id=amigo_id).exists():
            any_error =1
            dict_response['error'] = "El usuario que intentas agregar no existe"
                
        if user_id == amigo_id:
            any_error =1
            dict_response['error'] = "El usuario no puede ser amigo de si mismo"

        if any_error ==0:
            usuario_instance = get_object_or_404(Usuario, id=user_id)
            amigo_instance = get_object_or_404(Usuario, id=amigo_id)
            amigo_db = Amigos.objects.create(user_id=usuario_instance,amigo_id=amigo_instance)
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
        user_id, token = get_userID_and_token(request)

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
        elif not nombre_sala.isascii():
            any_error = 1
            dict_response['error_nombre_sala'] = "La sala tiene caracteres no permitidos"
            
        #Check tipo_sala
        if tipo_sala not in dict(Sala.SALA_CHOICES):
            any_error = 1
            dict_response['error_tipo_sala'] = "Solo son validos: Publico,Privado"

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
            dict_response['error_tiempo_respuesta'] = "Tiempo de respuesta invalido(10-50)"

        if any_error ==0:
            usuario_instance = get_object_or_404(Usuario, id=user_id)
            # Creamos la sala
            sala = Sala.objects.create(nombre_sala=nombre_sala,creador_id=usuario_instance,tiempo_respuesta=tiempo_respuesta
                                       ,n_jugadores=n_jugadores,password_sala=password_sala,tipo_partida=tipo_partida,tipo_sala=tipo_sala)
            sala.set_password(password_sala)
            sala.save()
            sala_usuario = UsuariosSala.objects.create(nombre_sala=sala,user_id=usuario_instance,equipo=1)
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
        user_id, token = get_userID_and_token(request)
        nombre_sala = request.data.get('nombre_sala')
        sala = Sala.objects.filter(nombre_sala=nombre_sala).first() or None
        usuario_instance = Usuario.objects.filter(id=user_id).first() or None
        #Check if sala exists
        if sala:
            jugadores_en_partida =  UsuariosSala.objects.filter(nombre_sala=nombre_sala).count()
            if(jugadores_en_partida > sala.n_jugadores):
                any_error = 1
                dict_response['error_sala'] = "La sala esta llena, no puedes unirte"
            
            usuario_sala = UsuariosSala.objects.filter(nombre_sala=nombre_sala,user_id=usuario_instance).first() or None
            if(usuario_sala):
                any_error = 1
                dict_response['error_sala'] = "Ya perteneces a esta sala, no puedes unirte"
        else:
            any_error = 1
            dict_response['error_sala'] = "La sala no existe"
            
        if any_error ==0:
            sala_usuario = UsuariosSala.objects.create(nombre_sala=sala,user_id=usuario_instance,equipo=1)
            sala_usuario.save()
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        return Response(dict_response)


class SalaLista(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # token = get_token(request)
        # username = Token.objects.get(key=token).user

        salas = Sala.objects.all()
        serializer = SalaSerializer(salas, many=True)
        return Response(serializer.data)


#Lista los jugadores y el equipo al que pertencen en la sala especificada
class SalaListaJugadoresSala(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id, token = get_userID_and_token(request)
        nombre_sala = request.data.get('nombre_sala')
        sala = Sala.objects.filter(nombre_sala=nombre_sala).first() or None
        if(sala):
            # Filter Sala objects based on nombre
            usuarios = UsuariosSala.objects.filter(nombre_sala=sala)
            # Get list of usernames
            usernames = [{'username': str(usuario.user_id),'equipo': str(usuario.equipo)} for usuario in usuarios]
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