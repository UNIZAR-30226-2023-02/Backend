from django.shortcuts import render, get_object_or_404
from .models import *
from sala.models import *
from partida.models import *
from .serializers import *
from trivial_api.funciones_auxiliares import *

# Auxiliar
import re
from datetime import datetime

# API views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# API documentacion
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes

# Token
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

# Imagenes
import os
from django.conf import settings
from django.conf.urls.static import static


# Añadir a la documentacion, si se requiere del Token
header = OpenApiParameter(
    name='Authorization',
    location=OpenApiParameter.HEADER,
    type=OpenApiTypes.STR,
    required=True,
    description='Authentication token',
)


# BORRAR
class MonedasInfinitas(APIView):
    '''
    Loguea al usuario, en caso correcto devolvera el token del usuario.
    '''
    def post(self, request):
        username, token = get_username_and_token(request)
        monedas = int(request.data.get('monedas'))
        user = Usuario.objects.filter(username=username).first() or None
        # Retrieve the credentials from the request data
        if(user):
            user.monedas = monedas
            user.save()
        return Response("monedas")
        






class UsuarioLogin(APIView):
    '''
    Loguea al usuario, en caso correcto devolvera el token del usuario.
    '''
    @extend_schema(tags=["USUARIO"],request=UsuarioLoginRequestSerializer, responses=UsuarioLoginResponseSerializer)
    def post(self, request):
        dict_response = {
            'OK':"",
            'token':"",
            'error_username': "",
            'error_password': "",
        }
        # Retrieve the credentials from the request data
        username = str(request.data.get('username'))
        password = str(request.data.get('password'))
        # Comprobacion de errores
        # Busca si existe el usuario, si no existe guarda None en user
        user = Usuario.objects.filter(username=username).first() or None
        if user == None:
            dict_response['error_username'] = "Usuario invalido"
        
        if user and not user.check_password(password):
            dict_response['error_password'] = "Contraseña invalida"

        if all_errors_empty(dict_response):
            #Se crea un token asociado al usuario, si es la primera vez que inicia.
            #en caso contrario obtiene dicho token
            token,_ = Token.objects.get_or_create(user=user)
            dict_response['token'] = token.key
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        
        return Response(dict_response)


class UsuarioRegistrar(APIView):
    '''
    Crea un nuevo usuario si no se produce ningún error.
    '''
    @extend_schema(tags=["USUARIO"],request=UsuarioRegistrarRequestSerializer, responses=UsuarioRegistrarResponseSerializer)
    def post(self, request):
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

        username = str(request.data.get('username'))
        password = str(request.data.get('password'))
        confirm_password = str(request.data.get('confirm_password'))
        fecha_nac = str(request.data.get('fecha_nac'))
        correo = str(request.data.get('correo'))
        telefono = str(request.data.get('telefono'))
        esAdmin = request.data.get('esAdmin')

        # Check username
        dict_response["error_username"] = validate_username_register(username)
        # Check password
        dict_response["error_password"], \
        dict_response["error_confirm_password"] = validate_password_register(password,confirm_password)
        # Check correo
        dict_response["error_correo"] = validate_correo_register(correo)
        # Check telefono
        dict_response["error_telefono"] = validate_telefono(telefono)
        # Check fecha nacimiento
        dict_response["error_fecha_nac"] = validate_fecha_nac(fecha_nac)

        # Si no hay errores
        if all_errors_empty(dict_response):
            # Creamos el registro en la base de datos
            user = Usuario.objects.create(username=username, correo=correo,telefono = telefono,fecha_nac=fecha_nac,password=password)
            user.set_password(password)
            # Ficha y tablero por defecto
            objeto_ficha = Objetos.objects.filter(id=1).first()
            objeto_tablero = Objetos.objects.filter(id=20).first()
            user.image_ficha = objeto_ficha.image
            user.image_tablero = objeto_tablero.image
            print(esAdmin)
            if(esAdmin):
                user.esAdmin = esAdmin
            user.save()

            # Hay que hacer que tenga la ficha y el tablero por defecto 
            tiene_objeto_ficha = Tiene.objects.create(id_objeto=objeto_ficha,username = user,enUso=1)
            tiene_objeto_tablero = Tiene.objects.create(id_objeto=objeto_tablero,username = user,enUso=1)
            
            tiene_objeto_ficha.save()
            tiene_objeto_tablero.save()
            
            # Hay que crear la instancia de las esatdisticas
            stats = Estadisticas.objects.create(username = user)
            stats.save()

            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        return Response(dict_response)


class UsuarioDatos(APIView):
    '''
    Muestra los datos del usuario que los solicita.
    '''
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["USUARIO"],parameters=[header],request=UsuarioDatosRequestSerializer, responses=UsuarioDatosResponseSerializer)
    def post(self, request):
        username, token = get_username_and_token(request)
        print("EL NOMBRE : " + username)
        dict_response = {
            'OK':"",
            'username':"",
            'correo': "",
            'telefono':"",
            'fecha_nac': "",
            'monedas': "",
            'imagen_perfil':"",
            'amigos':[],
        }
        user = Usuario.objects.filter(username=username).first() or None
        if user:
            # Solo muestro los amigos que he aceptado
            amigos = Amigos.objects.filter(user1=username,pendiente=False)
            dict_response['username'] = user.username
            dict_response['correo'] = user.correo
            dict_response['fecha_nac'] = user.fecha_nac
            dict_response['monedas'] = user.monedas   
            dict_response['telefono'] = user.telefono  

            dict_response['imagen_perfil'] = user.image_perfil if user.image_perfil else ''
            
            for amigo in amigos:
                dict_response['amigos'].append(str(amigo.user2)) 
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        return Response(dict_response)


class UsuarioDatosOtroUsuario(APIView):
    '''
    Muestra los datos del usuario que los solicita.
    '''
    @extend_schema(tags=["USUARIO"],request=UsuarioDatosOtroUsuarioRequestSerializer, responses=UsuarioDatosOtroUsuarioResponseSerializer)
    def post(self, request):
        username = request.data.get("username")
        dict_response = {
            'OK':"",
            'username':"",
            'correo': "",
            'telefono':"",
            'fecha_nac': "",
            'monedas': "",
            'imagen_perfil':"",
            'amigos':[]
        }
        user = Usuario.objects.filter(username=username).first() or None
        if user:
            # Solo muestro los amigos que he aceptado
            amigos = Amigos.objects.filter(user1=username,pendiente=False)
            dict_response['username'] = user.username
            dict_response['correo'] = user.correo
            dict_response['fecha_nac'] = user.fecha_nac
            dict_response['monedas'] = user.monedas   
            dict_response['telefono'] = user.telefono  
            dict_response['imagen_perfil'] = user.image_perfil if user.image_perfil else ''
            
            for amigo in amigos:
                dict_response['amigos'].append(str(amigo.user2)) 

            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        return Response(dict_response)


class UsuarioCambiarDatos(APIView):
    '''
    Actualiza los datos del usuario.
    '''
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["USUARIO"],parameters=[header],request=UsuarioCambiarDatosRequestSerializer, responses=UsuarioCambiarDatosResponseSerializer)
    def post(self, request):
        dict_response = {
            'OK':"",
            'error_correo':"",
            'error_fecha_nac':"",
            'error_telefono':"",
        }

        correo = str(request.data.get('correo'))
        telefono = str(request.data.get('telefono'))
        fecha_nac = str(request.data.get('fecha_nac'))

        username, token = get_username_and_token(request)
        user = Usuario.objects.filter(username=username).first() or None
        user_correo = Usuario.objects.filter(correo=correo).first() or None

        # Check correo
        dict_response["error_correo"] = validate_correo_cambiar_datos(correo,user_correo,username)
        # Check telefono
        dict_response["error_telefono"] = validate_telefono(telefono)
        dict_response["error_fecha_nac"] = validate_fecha_nac(fecha_nac)


        # Si tenemos errores
        if all_errors_empty(dict_response):
            # Creamos el registro en la base de datos
            user.username = username
            user.correo = correo
            user.fecha_nac = fecha_nac
            user.telefono = telefono
            user.save()
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        return Response(dict_response)




class UsuarioAddAmigo(APIView):
    '''
    Añade un amigo al usuario que lo solicita, si todo es correcto.
    '''
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["AMIGOS"],parameters=[header],request=UsuarioAddAmigoRequestSerializer, responses=UsuarioAddAmigoResponseSerializer)
    def post(self, request):
        #Con esto comprobamos si el usuario tiene acceso a la informacion
        username, token = get_username_and_token(request)
        amigo = request.data.get('amigo')
        
        dict_response = {
            'OK':"",
            'error':""
        }

        if not existe_usuario(username):
            dict_response['error'] = "El usuario no existe"
            
        if not existe_usuario(amigo):
            dict_response['error'] = "El usuario que intentas agregar no existe"

        if username == amigo:
            dict_response['error'] = "El usuario no puede ser amigo de si mismo"
        
        es_amigo = Amigos.objects.filter(user1=username,user2=amigo).first() or None
        if es_amigo:
            if(es_amigo.pendiente):
                dict_response['error'] = "Ya has enviado una peticion"
            else:
                dict_response['error'] = "Ya tienes el amigo agregado"
                
        if all_errors_empty(dict_response):
            usuario_instance = get_object_or_404(Usuario, username=username)
            amigo_instance = get_object_or_404(Usuario, username=amigo)

            # Esto es para que salga en la base de datos ambos como amigos pendientes, necesitan ser aceptados
            amigo_db = Amigos.objects.create(user1=usuario_instance,user2=amigo_instance,pendiente=True)
            amigo_db1 = Amigos.objects.create(user1=amigo_instance,user2=usuario_instance,pendiente=True)
            amigo_db.save()
            amigo_db1.save()
            dict_response['OK'] = "True"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)
    

class UsuarioDeleteAmigo(APIView):
    '''
    Elimina de tus amigos al usuario especificado
    '''
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["AMIGOS"],parameters=[header],request=UsuarioDeleteAmigoRequestSerializer, responses=UsuarioDeleteAmigoResponseSerializer)
    def post(self, request):
         #Con esto comprobamos si el usuario tiene acceso a la informacion
        username, token = get_username_and_token(request)
        amigo = request.data.get('amigo')
        
        dict_response = {
            'OK':"",
            'error':""
        }

        if not existe_usuario(username):
            dict_response['error'] = "El usuario no existe"
            
        if not existe_usuario(amigo):
            dict_response['error'] = "El usuario que intentas eliminar no existe"

        if username == amigo:
            dict_response['error'] = "El usuario no puede ser amigo de si mismo"

        es_amigo = Amigos.objects.filter(user1=username,user2=amigo).first() or None

        # No se puede eliminar a un amigo que no es tu amigo, o que este pendiente
        if not es_amigo or (es_amigo and es_amigo.pendiente):
            dict_response['error'] = "No puedes eliminarlo ya que no es tu amigo"
          
        if all_errors_empty(dict_response):
            usuario_instance = get_object_or_404(Usuario, username=username)
            amigo_instance = get_object_or_404(Usuario, username=amigo)
            # Eliminamos las dos instancias, ya que de momento si eliminamos en un lado se elimina en ambos
            amigo_db = Amigos.objects.filter(user1=usuario_instance,user2=amigo_instance).first()
            amigo_db1 = Amigos.objects.filter(user1=amigo_instance,user2=usuario_instance).first()
            amigo_db.delete()
            amigo_db1.delete()
            dict_response['OK'] = "True"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)



class UsuarioAceptarAmigo(APIView):
    '''
    Aceptar la invitacion de un amigo
    '''
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["AMIGOS"],parameters=[header],request=UsuarioAceptarAmigo1, responses=UsuarioAceptarAmigo2)
    def post(self, request):
        #Con esto comprobamos si el usuario tiene acceso a la informacion
        username, token = get_username_and_token(request)
        amigo = request.data.get('amigo')
        
        dict_response = {
            'OK':"",
            'error':""
        }
        es_amigo = Amigos.objects.filter(user1=username,user2=amigo).first() or None
        
        # No se puede eliminar a un amigo que no es tu amigo, o que este pendiente
        print(es_amigo)
        print(es_amigo.pendiente)
        if not (es_amigo and es_amigo.pendiente):
            dict_response['error'] = "No es una peticion de amigo"

        if all_errors_empty(dict_response):
            usuario_instance = get_object_or_404(Usuario, username=username)
            amigo_instance = get_object_or_404(Usuario, username=amigo)
            amigo_db = Amigos.objects.filter(user1=usuario_instance,user2=amigo_instance).first()
            amigo_db1 = Amigos.objects.filter(user1=amigo_instance,user2=usuario_instance).first()
            amigo_db.pendiente = False
            amigo_db1.pendiente = False
            amigo_db.save()
            amigo_db1.save()
            dict_response['OK'] = "True"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)



class UsuarioRechazarAmigo(APIView):
    '''
    Rechazar la invitacion de un amigo
    '''
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["AMIGOS"],parameters=[header],request=UsuarioRechazarAmigo1, responses=UsuarioRechazarAmigo2)
    def post(self, request):
        #Con esto comprobamos si el usuario tiene acceso a la informacion
        username, token = get_username_and_token(request)
        amigo = request.data.get('amigo')
        
        dict_response = {
            'OK':"",
            'error':""
        }
        es_amigo = Amigos.objects.filter(user1=username,user2=amigo).first() or None
        
        print(es_amigo)
        print(es_amigo.pendiente)
        # No se puede eliminar a un amigo que no es tu amigo, o que este pendiente
        if not (es_amigo and es_amigo.pendiente):
            dict_response['error'] = "No es una peticion de amigo"

        if all_errors_empty(dict_response):
            usuario_instance = get_object_or_404(Usuario, username=username)
            amigo_instance = get_object_or_404(Usuario, username=amigo)
            amigo_db = Amigos.objects.filter(user1=usuario_instance,user2=amigo_instance).first()
            amigo_db1 = Amigos.objects.filter(user1=amigo_instance,user2=usuario_instance).first()
            amigo_db.delete()
            amigo_db1.delete()
            dict_response['OK'] = "True"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)




class UsuarioListarPeticionesAmigo(APIView):
    '''
    Listar peticiones amigos
    '''
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["AMIGOS"],parameters=[header],request=UsuarioListarPeticionesAmigo1, responses=UsuarioListarPeticionesAmigo2)
    def post(self, request):
        #Con esto comprobamos si el usuario tiene acceso a la informacion
        username, token = get_username_and_token(request)
        amigo = request.data.get('amigo')
        
        dict_response = {
            'OK':"",
            'amigos_pendientes':[],
            'error':"",
        }

        # Solo muestro los amigos que he aceptado
        amigos = Amigos.objects.filter(user1=username,pendiente=True)
        for amigo in amigos:
            dict_response['amigos_pendientes'].append(str(amigo.user2)) 
        dict_response['OK'] = "True"
        return Response(dict_response)


class SalaCrear(APIView):
    '''
    Crea una nueva sala si todo es correcto
    '''
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["SALA"],parameters=[header],request=SalaCrearRequestSerializer, responses=SalaCrearResponseSerializer)
    def post(self, request):
        any_error = 0
        dict_response = {
            'OK':"",
            'websocket':"",
            'error_nombre_sala':"",
            'error_tipo_sala':"",
            'error_tipo_partida':"",
            'error_n_jugadores':"",
            'error_tiempo_respuesta':"",
            'error_tematica':"",
        }
        username, token = get_username_and_token(request)

        nombre_sala = str(request.data.get('nombre_sala')).replace(" ","_")
        tiempo_respuesta = int(request.data.get('tiempo_respuesta'))
        password_sala = str(request.data.get('password_sala'))
        n_jugadores = int(request.data.get('n_jugadores'))
        tipo_partida = str(request.data.get('tipo_partida'))
        tematica = str(request.data.get('tematica'))
        
        user = Usuario.objects.filter(username=username).first() or None
        
        if rechazar_reconexion(user):
            dict_response['error_tipo_sala'] = "Ya tienes una partida activa"

        if password_sala:
            tipo_sala = "Privado"
        else:
            tipo_sala = "Publico"

        # Check nombre_sala
        dict_response["error_nombre_sala"] = validate_sala_crear(nombre_sala)

        # Check tipo_sala
        if tipo_sala not in dict(Sala.SALA_CHOICES):
            dict_response['error_tipo_sala'] = "Solo son validos: Publico,Privado"

        # Check tipo_partida
        if tipo_partida not in dict(Sala.PARTIDA_CHOICES):
            dict_response['error_tipo_partida'] = "Solo son validos: Clasico,Equipo,Tematico"

        # Check n_jugadores
        if(n_jugadores <2 or n_jugadores>6):
            dict_response['error_n_jugadores'] = "El numero de jugadores tiene que ser entre 2 y 6"

        # Check tiempo_respuesta
        if(tiempo_respuesta <10 or tiempo_respuesta >50):
            dict_response['error_tiempo_respuesta'] = "Tiempo de respuesta invalido (10-50)"
            
        if(tipo_partida == "Tematico"):
            if(tematica != "Deportes" and tematica != "Arte" and tematica != "Entretenimiento" and tematica != "Historia" 
            and tematica != "Ciencia" and tematica != "Geografia" ):
                dict_response['error_tematica'] = "Tematica invalida"

        if all_errors_empty(dict_response):
            usuario_instance = get_object_or_404(Usuario, username=username)
            # Creamos la sala
            sala = Sala.objects.create(nombre_sala=nombre_sala,creador_username=usuario_instance,tiempo_respuesta=tiempo_respuesta
                                       ,n_jugadores=n_jugadores,password_sala=password_sala,tipo_partida=tipo_partida,tipo_sala=tipo_sala, tematica=tematica)
            sala.set_password(password_sala)
            sala.save()
            dict_response['OK'] = "True"
            dict_response['websocket'] = "/ws/lobby/" + nombre_sala + "/"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)




class SalaLista(APIView):
    '''
    Lista con todas las salas
    '''
    @extend_schema(tags=["SALA"], request=SalaListaRequestSerializer,responses=SalaListaResponseSerializer(many=True))
    def post(self, request):
        salas = Sala.objects.all()
        serializer = SalaListaResponseSerializer(salas, many=True)
        return Response(serializer.data)


#Lista los jugadores y el equipo al que pertencen en la sala especificada
class SalaListaJugadores(APIView):
    '''
    Lista con todos los usuarios de una sala
    '''
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["SALA"], parameters=[header],request=SalaListaJugadoresRequestSerializer,responses=SalaListaJugadoresResponseSerializer)
    def post(self, request):
        dict_response = {
            "usuarios":[]
        }
        username, token = get_username_and_token(request)
        nombre_sala = str(request.data.get('nombre_sala'))
        sala = Sala.objects.filter(nombre_sala=nombre_sala).first() or None
        if(sala):
            # Filter Sala objects based on nombre
            usuarios = UsuariosSala.objects.filter(nombre_sala=sala)
            # Get list of usernames and equipo
            info_user = [{'username': str(usuario.username),'equipo': str(usuario.equipo)} for usuario in usuarios]
        else:
            info_user = []
        dict_response["usuarios"] = info_user
        return Response(dict_response)



class UsuarioEstadisticasYo(APIView):
    '''
    Estadisticas de mi usuario
    '''
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["USUARIO"],parameters=[header],request=UsuarioEstadisticasYoRequestSerializer, responses=UsuarioEstadisticasYoResponseSerializer)
    def post(self, request):
        dict_response = {
            'OK':"",
            'geografia':{"total":"","bien":"","mal":"","porcentaje":""},
            'arte_y_literatura':{"total":"","bien":"","mal":"","porcentaje":""},
            'historia':{"total":"","bien":"","mal":"","porcentaje":""},
            'entretenimiento':{"total":"","bien":"","mal":"","porcentaje":""},
            'ciencias':{"total":"","bien":"","mal":"","porcentaje":""},
            'deportes':{"total":"","bien":"","mal":"","porcentaje":""},
            'quesitos_totales':"",
            'total_preguntas':"",
            'total_respuestas_correctas':"",
            'total_respuestas_incorrectas':"",
            'porcentaje_respuestas':"",
            'total_partidas':"",
            'total_partidas_ganadas':"",
            'total_partidas_perdidas':"",
            'porcentaje_partidas':"",
            'error_usuario':"",
        }
        username, token = get_username_and_token(request)
        user = Usuario.objects.filter(username=username).first() or None
        stats = Estadisticas.objects.filter(username=user).first() or None
        total_respuestas_correctas = 0
        total_respuestas_incorrectas = 0
        if(user):
            categorias = ["geografia","arte_y_literatura","historia","entretenimiento","ciencias","deportes"]
            for categoria in categorias:
                bien_categoria = getattr(stats, f"{categoria}_bien")
                mal_categoria = getattr(stats, f"{categoria}_mal")
                total_categoria = bien_categoria + mal_categoria
                dict_response[categoria]["total"] =  str(total_categoria)
                dict_response[categoria]["bien"] = str(bien_categoria)
                dict_response[categoria]["mal"] = str(mal_categoria)
                if total_categoria == 0:
                    dict_response[categoria]["porcentaje"] = "0"
                else:
                    porcentaje = (bien_categoria / total_categoria) * 100
                    dict_response[categoria]["porcentaje"] = str(round(porcentaje,2))
                total_respuestas_correctas += bien_categoria
                total_respuestas_incorrectas += mal_categoria

            total_preguntas = total_respuestas_correctas + total_respuestas_incorrectas
            dict_response["quesitos_totales"] = str(stats.quesitos)
            dict_response["total_preguntas"] = str(total_preguntas)
            dict_response["total_respuestas_correctas"] = str(total_respuestas_correctas)
            dict_response["total_respuestas_incorrectas"] = str(total_respuestas_incorrectas)
            total_partidas = stats.partidas_ganadas + stats.partidas_perdidas
            dict_response['total_partidas'] = str(total_partidas)
            dict_response['total_partidas_ganadas'] = str(stats.partidas_ganadas)
            dict_response['total_partidas_perdidas'] = str(stats.partidas_perdidas)
            if total_preguntas == 0:
                dict_response["porcentaje_respuestas"] = "0"
            else:
                porcentaje = (total_respuestas_correctas / total_preguntas) * 100
                dict_response["porcentaje_respuestas"] = str(round(porcentaje,2))
            
            if total_partidas == 0:
                dict_response["porcentaje_partidas"] = 0
            else:
                porcentaje = (stats.partidas_ganadas / total_partidas) * 100
                dict_response["porcentaje_partidas"] = str(round(porcentaje,2))
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
            dict_response["error_usuario"] = "No se ha encontrado el usuario"
        #serializer = UsuarioEstadisticasYoResponseSerializer(dict_response)
        return Response(dict_response)
    

class UsuarioEstadisticasOtroUsuario(APIView):
    '''
    Estadisticas del usuario que paso como parametro
    '''
    @extend_schema(tags=["USUARIO"],request=UsuarioEstadisticasRequestSerializer, responses=UsuarioEstadisticasYoResponseSerializer)
    def post(self, request):
        dict_response = {
            'OK':"",
            'geografia':{"total":"","bien":"","mal":"","porcentaje":""},
            'arte_y_literatura':{"total":"","bien":"","mal":"","porcentaje":""},
            'historia':{"total":"","bien":"","mal":"","porcentaje":""},
            'entretenimiento':{"total":"","bien":"","mal":"","porcentaje":""},
            'ciencias':{"total":"","bien":"","mal":"","porcentaje":""},
            'deportes':{"total":"","bien":"","mal":"","porcentaje":""},
            'quesitos_totales':"",
            'total_preguntas':"",
            'total_respuestas_correctas':"",
            'total_respuestas_incorrectas':"",
            'porcentaje_respuestas':"",
            'total_partidas':"",
            'total_partidas_ganadas':"",
            'total_partidas_perdidas':"",
            'porcentaje_partidas':"",
            'error_usuario':"",
        }
        username = request.data.get('username')
        user = Usuario.objects.filter(username=username).first() or None
        stats = Estadisticas.objects.filter(username=user).first() or None
        total_respuestas_correctas = 0
        total_respuestas_incorrectas = 0
        if(user):
            categorias = ["geografia","arte_y_literatura","historia","entretenimiento","ciencias","deportes"]
            for categoria in categorias:
                bien_categoria = getattr(stats, f"{categoria}_bien")
                mal_categoria = getattr(stats, f"{categoria}_mal")
                total_categoria = bien_categoria + mal_categoria
                dict_response[categoria]["total"] =  str(total_categoria)
                dict_response[categoria]["bien"] = str(bien_categoria)
                dict_response[categoria]["mal"] = str(mal_categoria)
                if total_categoria == 0:
                    dict_response[categoria]["porcentaje"] = "0"
                else:
                    porcentaje = (bien_categoria / total_categoria) * 100
                    dict_response[categoria]["porcentaje"] = str(round(porcentaje,2))
                total_respuestas_correctas += bien_categoria
                total_respuestas_incorrectas += mal_categoria

            total_preguntas = total_respuestas_correctas + total_respuestas_incorrectas
            dict_response["quesitos_totales"] = str(stats.quesitos)
            dict_response["total_preguntas"] = str(total_preguntas)
            dict_response["total_respuestas_correctas"] = str(total_respuestas_correctas)
            dict_response["total_respuestas_incorrectas"] = str(total_respuestas_incorrectas)
            total_partidas = stats.partidas_ganadas + stats.partidas_perdidas
            dict_response['total_partidas'] = str(total_partidas)
            dict_response['total_partidas_ganadas'] = str(stats.partidas_ganadas)
            dict_response['total_partidas_perdidas'] = str(stats.partidas_perdidas)
            if total_preguntas == 0:
                dict_response["porcentaje_respuestas"] = "0"
            else:
                porcentaje = (total_respuestas_correctas / total_preguntas) * 100
                dict_response["porcentaje_respuestas"] = str(round(porcentaje,2))
            if total_partidas == 0:
                dict_response["porcentaje_partidas"] = 0
            else:
                porcentaje = (stats.partidas_ganadas / total_partidas) * 100
                dict_response["porcentaje_partidas"] = str(round(porcentaje,2))
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
            dict_response["error_usuario"] = "No se ha encontrado el usuario"
        #serializer = UsuarioEstadisticasYoResponseSerializer(dict_response)
        return Response(dict_response)
    


class TiendaObjetos(APIView): 
    '''
    Lista con las fichas y tableros
    '''
    permission_classes = [IsAuthenticated]
    #@extend_schema(exclude=True)
    @extend_schema(tags=["TIENDA"],parameters=[header],request=TiendaObjetosRequestSerializer, responses=TiendaObjetosResponseSerializer)
    def post(self, request):
        dict_response = {
            'fichas':[],
            'tableros':[],
            'monedas':"",
        }
        username, token = get_username_and_token(request)
        user = Usuario.objects.filter(username=username).first() or None
        # Obtenemos las fichas
        fichas = Objetos.objects.filter(tipo="ficha")
        for ficha in fichas:
            adquirido = 0
            enUso = 0
            tieneFicha = Tiene.objects.filter(id_objeto=str(ficha.id),username = username).first() or None
            if(tieneFicha):
                adquirido = 1
                enUso = tieneFicha.enUso
            dict_response['fichas'].append({"id": ficha.id, "coste": ficha.coste, "enUso": enUso, "adquirido": adquirido, "imagen": ficha.image}) 
        
        # Obtenemos los tableros
        tableros = Objetos.objects.filter(tipo="tablero")
        for tablero in tableros:
            adquirido = 0
            enUso = 0
            tieneTablero = Tiene.objects.filter(id_objeto=str(tablero.id),username = username).first() or None
            if(tieneTablero):
                adquirido = 1
                enUso = tieneTablero.enUso
            dict_response['tableros'].append({"id": tablero.id, "coste": tablero.coste, "enUso": enUso, "adquirido": adquirido, "imagen": tablero.image}) 
        
        dict_response['monedas'] = str(user.monedas)
        return Response(dict_response)
  


class ComprarObjeto(APIView):
    '''
    Comprar el objeto pasado como parametro
    '''
    permission_classes = [IsAuthenticated]
    #@extend_schema(exclude=True)
    @extend_schema(tags=["TIENDA"],parameters=[header],request=ComprarObjetoRequestSerializer, responses=ComprarObjetoResponseSerializer)
    def post(self, request):
        dict_response = {
            'OK':"",
            'error':"",
        }
        username, token = get_username_and_token(request)
        objeto_id = str(request.data.get('objeto_id'))
        
        user = Usuario.objects.filter(username=username).first() or None
        objeto = Objetos.objects.filter(id=objeto_id).first() or None
        # Si existe el usuario y el objeto
        if(user and objeto):
            monedas_usuario = user.monedas
            coste_objeto = objeto.coste
            tieneObjeto = Tiene.objects.filter(id_objeto=objeto,username = username).first() or None
            # Si no tiene el objeto comprado
            if(not tieneObjeto):
                # Si tiene el saldo suficiente
                if(monedas_usuario < coste_objeto):
                    dict_response["error"] = "El usuario no tiene el saldo suficiente"   
            else:
                dict_response["error"] = "El usuario ya tiene el objeto"
        else:
            dict_response["error"] = "Error al comprar"

        if(all_errors_empty(dict_response)):
            objeto_usuario = Tiene.objects.create(id_objeto=objeto,username = user)
            user.monedas = monedas_usuario - coste_objeto
            objeto_usuario.save()
            user.save()
            dict_response["OK"] = "True"
        else:
            dict_response["OK"] = "False"

        return Response(dict_response)
  

class UsarObjeto(APIView):
    '''
    El usuario tendrá en uso el objeto pasado como parametro
    '''
    permission_classes = [IsAuthenticated]
    #@extend_schema(exclude=True)
    @extend_schema(tags=["TIENDA"],parameters=[header],request=UsarObjetoRequestSerializer, responses=UsarObjetoResponseSerializer)
    def post(self, request):
        dict_response = {
            'OK':"",
            'error':"",
        }
        username, token = get_username_and_token(request)
        objeto_id = str(request.data.get('objeto_id'))
        
        user = Usuario.objects.filter(username=username).first() or None
        objeto = Objetos.objects.filter(id=objeto_id).first() or None
        if(user and objeto):
            tieneObjeto = Tiene.objects.filter(id_objeto=objeto,username = user).first() or None
            # Si no tiene el objeto comprado
            if(not tieneObjeto):
                dict_response["error"] = "Compra el objeto para poder usarlo"
        else:
            dict_response["error"] = "Error al asignar el objeto"
        if(all_errors_empty(dict_response)):
            # Actualizamos la imagen del tablero/ficha a la nueva 
            if(objeto.tipo == "ficha"):
                user.image_ficha = objeto.image
            elif(objeto.tipo == "tablero"):
                user.image_tablero = objeto.image
            
            objetos_de_un_tipo = Objetos.objects.filter(tipo=objeto.tipo)
            for objeto_1 in objetos_de_un_tipo:
                tiene_objeto_anterior = Tiene.objects.filter(id_objeto=objeto_1,username=user,enUso=1).first() or None
                if(tiene_objeto_anterior):
                    break            

            tiene_objeto_anterior.enUso = 0
            tieneObjeto.enUso = 1
            tiene_objeto_anterior.save()
            tieneObjeto.save()
            user.save()
            dict_response["OK"] = "True"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)








#Compruebo que la sala exista, que no este llena, y que no este unido a ninguna sala
class SalaValidarUnir(APIView):
    '''
    Si el usuario puede unirse a la sala le devolvera el websocket para unirse a la sala
    '''
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["SALA"],parameters=[header],request=SalaUnirRequestSerializer, responses=SalaUnirResponseSerializer)
    def post(self, request):
        dict_response = {
            'OK':"",
            'error_sala':"",
            'ws':"",
        }

        username, token = get_username_and_token(request)
        nombre_sala = str(request.data.get('nombre_sala'))
        password = str(request.data.get('password_sala'))
        

        sala = Sala.objects.filter(nombre_sala=nombre_sala).first() or None
        user = Usuario.objects.filter(username=username).first() or None
        
        #Check if sala exists
        if sala and user :
            if not rechazar_reconexion(user):
                usuario_en_sala = UsuariosSala.objects.filter(username=user).first() or None
                #Check if the user is already in a sala
                if(not usuario_en_sala):
                    jugadores_en_partida =  UsuariosSala.objects.filter(nombre_sala=nombre_sala).count()
                    if(jugadores_en_partida >= sala.n_jugadores):
                        dict_response['error_sala'] = "La sala esta llena, no puedes unirte"
                    if(sala.tipo_sala == "Privado" and (not sala.check_password(password))):
                        dict_response['error_sala'] = "Contraseña incorrecta"
                else:
                    dict_response['error_sala'] = "Ya perteneces a una sala, no puedes unirte"  
            else:
                dict_response['error_sala'] = "Ya perteneces a una partida activa, no puedes unirte"                
        else:
            dict_response['error_sala'] = "La sala no existe"
            
        if all_errors_empty(dict_response):
            dict_response['OK'] = "True"
            dict_response["ws"] = "/ws/lobby/{0}/?username={1}&password={2}".format(nombre_sala,username,password)
        else:
            dict_response['OK'] = "False"
        return Response(dict_response)






# Lista con las partidas activas de un usuario, para que pueda volver a unirse
class PartidaActiva(APIView):
    '''
    Muestra la partida que este activa, si no hay no muestra el websocket y mostrara error de no partidas activas
    '''
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["PARTIDA"],parameters=[header],request=PartidaActivaRequestSerializer, responses=PartidaActivaResponseSerializer)   
    def post(self,request):
        dict_response = {
            'OK':"",
            'ws_partida':'',
            'tipo':'',
            'error':"",
        }
        username, token = get_username_and_token(request)
        user = Usuario.objects.filter(username=username).first() or None
        juega = Juega.objects.filter(username=user).last() or None
        if juega and not juega.activo:
            partida = Partida.objects.filter(id=juega.id_partida.id).first() or None
            if(partida and not partida.terminada):
                if partida.tipo == "Clasico":
                    ws_partida = "/ws/partida/" + str(partida.id) + "/"
                    dict_response['Tipo'] = "Clasico"
                elif partida.tipo == "Tematico":
                    ws_partida = "/ws/partida_tematico/" + str(partida.id) + "/"
                    dict_response['Tipo'] = "Tematico"
                elif partida.tipo == "Equipo":
                    ws_partida = "/ws/partida_tematico/" + str(partida.id) + "/"
                    dict_response['Tipo'] = "Equipo"
                dict_response['ws_partida'] = ws_partida
            else:
                dict_response["error"] = "No hay partidas activas"
        else:
            dict_response["error"] = "No hay partidas activas"
        if all_errors_empty(dict_response):
            dict_response["OK"] = "True"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)
    

class UsuarioDarDeBaja(APIView):
    '''
    Elimina al usuario de la base de datos
    '''
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["USUARIO"],parameters=[header],request=UsuarioDarBajaRequestSerializer, responses=UsuarioDarBajaResponseSerializer)   
    def post(self,request):
        username, token = get_username_and_token(request)
        user = Usuario.objects.filter(username=username).first() or None
        if(user):
            user.delete()
        return Response("Deleted")




class EliminarPregunta(APIView):
    '''
    Elimina la pregunta de la base de datos
    '''
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["ADMIN"],parameters=[header],request=EliminarPregunta1, responses=EliminarPregunta2)   
    def post(self,request):
        dict_response = {
            'OK':"",
            'error':"",
        }
        username, token = get_username_and_token(request)
        user = Usuario.objects.filter(username=username).first() or None
        id = int(request.data.get('id'))

        if(user and user.esAdmin):
            pregunta = Pregunta.objects.filter(id=id).first() or None
            if pregunta:
                pregunta.delete()
                dict_response["OK"] = "True"
            else:
                dict_response["OK"] = "False"
                dict_response["error"] = "No existe la pregunta"
        else:
            dict_response["OK"] = "False"
            dict_response["error"] = "No eres admin"
        return Response(dict_response)


class AddPregunta(APIView):
    '''
    Añade la pregunta a la base de datos
    '''
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["ADMIN"],parameters=[header],request=AddPregunta1, responses=AddPregunta2)   
    def post(self,request):
        dict_response = {
            'OK':"",
            'error':"",
        }
        username, token = get_username_and_token(request)
        user = Usuario.objects.filter(username=username).first() or None
        
        enunciado = str(request.data.get('enunciado'))
        r1 = str(request.data.get('r1'))
        r2 = str(request.data.get('r2'))
        r3 = str(request.data.get('r3'))
        r4 = str(request.data.get('r4'))
        rc = request.data.get('rc')
        if(rc and rc.isdigit()):
            rc = int(request.data.get('rc'))
        else:
            dict_response["OK"] = "False"
            dict_response["error"] = "Formato incorrecto"
            return Response(dict_response)
        
        categoria = str(request.data.get('categoria'))
        
        if(user and user.esAdmin):
            pregunta_igual = Pregunta.objects.filter(enunciado=enunciado).first() or None
            if(not pregunta_igual):
                pregunta = Pregunta.objects.create(enunciado=enunciado,r1=r1,r2=r2,r3=r3,r4=r4,rc=rc,categoria=categoria)
                pregunta.save()
                dict_response["OK"] = "True"
            else:
                dict_response["OK"] = "False"
                dict_response["error"] = "No puede haber preguntas repetidas"
        else:
            dict_response["OK"] = "False"
            dict_response["error"] = "No eres admin"
        return Response(dict_response)
    


class EditPregunta(APIView):
    '''
    Edita la pregunta de la base de datos
    '''
    #permission_classes = [IsAuthenticated]
    @extend_schema(tags=["ADMIN"],parameters=[header],request=EditPregunta1, responses=EditPregunta2)   
    def post(self,request):
        dict_response = {
            'OK':"",
            'error':"",
        }
        username, token = get_username_and_token(request)
        user = Usuario.objects.filter(username=username).first() or None

        id = int(request.data.get('id'))
        enunciado = str(request.data.get('enunciado'))
        r1 = str(request.data.get('r1'))
        r2 = str(request.data.get('r2'))
        r3 = str(request.data.get('r3'))
        r4 = str(request.data.get('r4'))
        rc = request.data.get('rc')
        if(rc and rc.isdigit()):
            rc = int(request.data.get('rc'))
        else:
            dict_response["OK"] = "False"
            dict_response["error"] = "Formato incorrecto"
            return Response(dict_response)
        
        categoria = str(request.data.get('categoria'))
        
        if(user and user.esAdmin):
            pregunta_repetida = Pregunta.objects.filter(enunciado=enunciado).first() or None
            pregunta = Pregunta.objects.filter(id=id).first() or None
            
            if pregunta_repetida and not pregunta.id==pregunta_repetida.id:
                dict_response["error"] = "Pregunta repetida"
            elif pregunta:
                pregunta.enunciado = enunciado
                pregunta.r1 = r1
                pregunta.r2 = r2
                pregunta.r3 = r3
                pregunta.r4 = r4
                pregunta.rc = rc
                pregunta.categoria = categoria
                pregunta.save()
                dict_response["OK"] = "True"
            else:
                dict_response["OK"] = "False"
                dict_response["error"] = "No existe la pregunta que buscas"
        else:
            dict_response["OK"] = "False"
            dict_response["error"] = "No eres admin"
        return Response(dict_response)


class InfoPregunta(APIView):    
    '''
    Los datos necesarios para obtener la informacion de la pregunta
    '''
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["ADMIN"],parameters=[header],request=InfoPregunta1, responses=InfoPregunta2) 
    def post(self,request):
        dict_response = {
            'OK':"",
            'enunciado':"",
            'r1':"",
            'r2':"",
            'r3':"",
            'r4':"",
            'rc':"",
            'categoria':"",
            'error':"",
        }
        id = int(request.data.get('id'))

        pregunta = Pregunta.objects.filter(id=id).first() or None
        if pregunta:
            dict_response["enunciado"] = pregunta.enunciado
            dict_response["r1"] = pregunta.r1
            dict_response["r2"] = pregunta.r2
            dict_response["r3"] = pregunta.r3
            dict_response["r4"] = pregunta.r4
            dict_response["rc"] = pregunta.rc
            dict_response["categoria"] = pregunta.categoria
            dict_response["OK"] = "True"
        else:
            dict_response["OK"] = "False"
            dict_response["error"] = "No existe la pregunta seleccionada"
        return Response(dict_response)



class ListarPreguntas(APIView):
    '''
    Lista todas las preguntas de la base de datos
    '''
    @extend_schema(tags=["ADMIN"],parameters=[header],request=ListarPreguntas1, responses=ListarPreguntas2)   
    def post(self,request):
        dict_response = {
            'OK':"",
            'preguntas':[],
        }
        preguntas = Pregunta.objects.all()
        preguntas = list(preguntas)
        for pregunta in preguntas:
            dict_response["preguntas"].append({'enunciado':str(pregunta.enunciado),'id':str(pregunta.id)})
        dict_response["OK"] = "True"
        return Response(dict_response)


class AdminLogin(APIView):
    '''
    Solo se le permite acceder al administrador
    '''
    @extend_schema(tags=["ADMIN"],request=AdminLogin1, responses=AdminLogin2)
    def post(self, request):
        dict_response = {
            'OK':"",
            'token':"",
            'error_username': "",
            'error_password': "",
        }
        # Retrieve the credentials from the request data
        username = str(request.data.get('username'))
        password = str(request.data.get('password'))
        # Comprobacion de errores
        # Busca si existe el usuario, si no existe guarda None en user
        user = Usuario.objects.filter(username=username).first() or None
        if user == None:
            dict_response['error_username'] = "Usuario invalido"
        
        if user and not user.check_password(password):
            dict_response['error_password'] = "Contraseña invalida"

        if user and not user.esAdmin:
            dict_response['error_username'] = "No tienes acceso"

        if all_errors_empty(dict_response):
            #Se crea un token asociado al usuario, si es la primera vez que inicia.
            #en caso contrario obtiene dicho token
            token,_ = Token.objects.get_or_create(user=user)
            dict_response['token'] = token.key
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        
        return Response(dict_response)


# Cuando envio la peticion, estoy si o si en una sala, por lo que UsuariosSala tiene que tener la sala en la que estoy
class EnviarPeticionUnirSala(APIView):
    '''
    Enviar peticion a un amigo, le envio la sala en la que estoy
    '''
    @extend_schema(tags=["SALA"],parameters=[header],request=EnviarPeticionUnirSala1, responses=EnviarPeticionUnirSala2)
    def post(self, request):
        dict_response = {
            'OK':"",
            'error': "",
        }

        username, token = get_username_and_token(request)
        user = Usuario.objects.filter(username=username).first() or None
        username_amigo = str(request.data.get('username_amigo'))

        esAmigo = Amigos.objects.filter(user1=username,user2=username_amigo).first() or None
        usuario_sala = UsuariosSala.objects.filter(username=user).last() or None
        
        if(esAmigo):
            if(usuario_sala):
                user_amigo = Usuario.objects.filter(username=username_amigo).first() or None
                peticion_pendiente = PeticionesAmigo.objects.filter(user=user_amigo,peticion_amigo=user,sala_inv=usuario_sala.nombre_sala).first() or None
                if(not peticion_pendiente):
                    # Añado la peticion a la base de datos
                    peticion = PeticionesAmigo.objects.create(user=user_amigo,peticion_amigo=user,sala_inv=usuario_sala.nombre_sala)
                    peticion.save()
                else:
                    dict_response["error"] = "Ya has enviado una peticion"
            else:
                dict_response["error"] = "No existe la sala"
        else:
            dict_response["error"] = "No es tu amigo"
        if(all_errors_empty(dict_response)):
            dict_response["OK"] = "True"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)


class ListarPeticionesSala(APIView):
    '''
    Listo todas las peticiones que tenga 
    '''
    @extend_schema(tags=["SALA"],parameters=[header],request=ListarPeticionesSala1, responses=ListarPeticionesSala2)
    def post(self, request):
        dict_response = {
            'OK':"",
            'peticiones': [],
            'error':'',
        }
        username, token = get_username_and_token(request)
        user = Usuario.objects.filter(username=username).first() or None
        if rechazar_reconexion(user):
            dict_response['error'] = "No puedes aceptar peticiones ya que perteneces a una partida"
        
        peticiones_pendientes = list(PeticionesAmigo.objects.filter(user=user))
        
        for peticion in peticiones_pendientes:
            nombre_sala = str(peticion.sala_inv.nombre_sala)
            tipo_partida = str(peticion.sala_inv.tipo_partida)
            n_jugadores = int(peticion.sala_inv.n_jugadores)
            ws = "/ws/lobby/"  + nombre_sala + "/?username=" + username
            dict_response["peticiones"].append({"nombre_sala":nombre_sala,"tipo_partida":tipo_partida,"me_invita":str(peticion.peticion_amigo),"ws": ws,"n_jugadores":n_jugadores})
        if(all_errors_empty(dict_response)):
            dict_response["OK"] = "True"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)





# class PeticionesAmigo(models.Model):
#     user = models.ForeignKey(Usuario, on_delete = models.CASCADE, db_column = "user", related_name = 'user')
#     peticion_amigo = models.ForeignKey(Usuario, on_delete = models.CASCADE, db_column = "amigo_inv", related_name = 'amigo_inv')
#     sala_inv = models.ForeignKey(Sala,on_delete=models.CASCADE,db_column="sala_invitado",related_name='sala_invitado')
#     class Meta:
#             #Para indicar que la clave primaria es multiple
#             db_table = "Peticiones"

# class UsuariosSala(models.Model):
#     nombre_sala = models.ForeignKey(Sala,on_delete=models.CASCADE,db_column="nombre_sala",related_name='usuarios_sala_usuario_nombre_sala')
#     username = models.ForeignKey(Usuario,on_delete=models.CASCADE,db_column="username",related_name='usuarios_sala_usuario')
#     equipo = models.IntegerField(default=1)
#     class Meta:
#         constraints = [
#         models.UniqueConstraint(fields=['nombre_sala', 'username'], name='usuario_sala_pk')
#         ] 
#         db_table = "UsuariosSala"