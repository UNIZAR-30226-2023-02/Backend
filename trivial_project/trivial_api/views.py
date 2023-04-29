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
        username = request.data.get('username')
        password = request.data.get('password')

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

        username = request.data.get('username')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        fecha_nac = request.data.get('fecha_nac')
        correo = request.data.get('correo')
        telefono = request.data.get('telefono')


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
        
            objeto_ficha = Objetos.objects.filter(id=1).first()
            objeto_tablero = Objetos.objects.filter(id=2).first()
            user.image_ficha = objeto_ficha.image
            user.image_tablero = objeto_tablero.image
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
            amigos = Amigos.objects.filter(user1=username)
            amigos2 = Amigos.objects.filter(user2=username)
            dict_response['username'] = user.username
            dict_response['correo'] = user.correo
            dict_response['fecha_nac'] = user.fecha_nac
            dict_response['monedas'] = user.monedas   
            dict_response['telefono'] = user.telefono  

            dict_response['imagen_perfil'] = user.image_perfil if user.image_perfil else ''
            
            for amigo in amigos:
                dict_response['amigos'].append(str(amigo.user2)) 
            for amigo in amigos2:
                dict_response['amigos'].append(str(amigo.user1)) 

            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        return Response(dict_response)

# Funcion que devuelve los datos del usuario
# Uso: Para consultar los datos de otros usuarios
class UsuarioDatosOtroUsuario(APIView):
    '''
    Muestra los datos del usuario que introduces en el parametro 'username'.
    '''
    @extend_schema(tags=["USUARIO"],request=UsuarioDatosOtroUsuarioRequestSerializer, responses=UsuarioDatosOtroUsuarioResponseSerializer)
    def post(self, request):
        username = request.data.get('username')
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
            amigos = Amigos.objects.filter(user1=username)
            amigos2 = Amigos.objects.filter(user2=username)
            dict_response['username'] = user.username
            dict_response['correo'] = user.correo
            dict_response['fecha_nac'] = user.fecha_nac
            dict_response['monedas'] = user.monedas   
            dict_response['telefono'] = user.telefono  
            dict_response['imagen_perfil'] = user.imagen_perfil if user.imagen_perfil else ''
            
            for amigo in amigos:
                dict_response['amigos'].append(str(amigo.user2)) 
            for amigo in amigos2:
                dict_response['amigos'].append(str(amigo.user1)) 

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

        correo = request.data.get('correo')
        telefono = request.data.get('telefono')
        fecha_nac = request.data.get('fecha_nac')

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
    @extend_schema(tags=["USUARIO"],parameters=[header],request=UsuarioAddAmigoRequestSerializer, responses=UsuarioAddAmigoResponseSerializer)
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

        # Ordenamos alfabeticamente 
        if username > amigo:
            username , amigo = amigo,username

        if username == amigo:
            dict_response['error'] = "El usuario no puede ser amigo de si mismo"
        if es_amigo(username,amigo):
            dict_response['error'] = "Ya tienes el amigo agregado"
                
        if all_errors_empty(dict_response):
            usuario_instance = get_object_or_404(Usuario, username=username)
            amigo_instance = get_object_or_404(Usuario, username=amigo)
            amigo_db = Amigos.objects.create(user1=usuario_instance,user2=amigo_instance)
            amigo_db.save()
            dict_response['OK'] = "True"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)
    
#class UsuarioEstadisticas(APIView):


class SalaCrear(APIView):
    '''
    Crea una nueva sala si todo es correcto
    '''
    #Necesita la autenticazion
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=["SALA"],request=SalaCrearRequestSerializer, responses=SalaCrearResponseSerializer)
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
        username, token = get_username_and_token(request)

        nombre_sala = request.data.get('nombre_sala')
        tiempo_respuesta = request.data.get('tiempo_respuesta')
        password_sala = request.data.get('password_sala')
        n_jugadores = request.data.get('n_jugadores')
        tipo_partida = request.data.get('tipo_partida')
        

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
        if(int(n_jugadores) <2 or int(n_jugadores) >6):
            dict_response['error_n_jugadores'] = "El numero de jugadores tiene que ser entre 2 y 6"

        # Check tiempo_respuesta
        if(int(tiempo_respuesta) <10 or int(tiempo_respuesta) >50):
            dict_response['error_tiempo_respuesta'] = "Tiempo de respuesta invalido (10-50)"

        if all_errors_empty(dict_response):
            usuario_instance = get_object_or_404(Usuario, username=username)
            # Creamos la sala
            sala = Sala.objects.create(nombre_sala=nombre_sala,creador_username=usuario_instance,tiempo_respuesta=tiempo_respuesta
                                       ,n_jugadores=n_jugadores,password_sala=password_sala,tipo_partida=tipo_partida,tipo_sala=tipo_sala)
            sala.set_password(password_sala)
            sala.save()
            dict_response['OK'] = "True"
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
        nombre_sala = request.data.get('nombre_sala')
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
                dict_response[categoria]["total"] =  total_categoria
                dict_response[categoria]["bien"] = bien_categoria
                dict_response[categoria]["mal"] = mal_categoria
                if total_categoria == 0:
                    dict_response[categoria]["porcentaje"] = 0
                else:
                    dict_response[categoria]["porcentaje"] = bien_categoria / total_categoria
                total_respuestas_correctas += bien_categoria
                total_respuestas_incorrectas += mal_categoria

            total_preguntas = total_respuestas_correctas + total_respuestas_incorrectas
            dict_response["quesitos_totales"] = stats.quesitos
            dict_response["total_preguntas"] = total_preguntas
            dict_response["total_respuestas_correctas"] = total_respuestas_correctas
            dict_response["total_respuestas_incorrectas"] = total_respuestas_incorrectas
            if total_preguntas == 0:
                dict_response["porcentaje_respuestas"] = 0
            else:
                dict_response["porcentaje_respuestas"] = total_respuestas_correctas / total_preguntas
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
            dict_response["error_usuario"] = "No se ha encontrado el usuario"
        serializer = UsuarioEstadisticasYoResponseSerializer(dict_response)
        return Response(serializer.data)
    

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
                dict_response[categoria]["total"] =  total_categoria
                dict_response[categoria]["bien"] = bien_categoria
                dict_response[categoria]["mal"] = mal_categoria
                if total_categoria == 0:
                    dict_response[categoria]["porcentaje"] = 0
                else:
                    dict_response[categoria]["porcentaje"] = bien_categoria / total_categoria
                total_respuestas_correctas += bien_categoria
                total_respuestas_incorrectas += mal_categoria

            total_preguntas = total_respuestas_correctas + total_respuestas_incorrectas
            dict_response["quesitos_totales"] = stats.quesitos
            dict_response["total_preguntas"] = total_preguntas
            dict_response["total_respuestas_correctas"] = total_respuestas_correctas
            dict_response["total_respuestas_incorrectas"] = total_respuestas_incorrectas
            if total_preguntas == 0:
                dict_response["porcentaje_respuestas"] = 0
            else:
                dict_response["porcentaje_respuestas"] = total_respuestas_correctas / total_preguntas
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
            dict_response["error_usuario"] = "No se ha encontrado el usuario"
        serializer = UsuarioEstadisticasYoResponseSerializer(dict_response)
        return Response(serializer.data)
    


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
        }
        username, token = get_username_and_token(request)
        
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
        objeto_id = request.data.get('objeto_id')
        
        user = Usuario.objects.filter(username=username).first() or None
        objeto = Objetos.objects.filter(id=objeto_id).first() or None
        # Si existe el usuario y el objeto
        if(user and objeto):
            monedas_usuario = user.monedas
            coste_objeto = objeto.coste
            tieneObjeto = Tiene.objects.filter(id_objeto=str(objeto.id),username = username).first() or None
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
            objeto_usuario = Tiene.objects.create(id_objeto=str(objeto.id),username = username)
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
        objeto_id = request.data.get('objeto_id')
        
        user = Usuario.objects.filter(username=username).first() or None
        objeto = Objetos.objects.filter(id=objeto_id).first() or None
        if(user and objeto):
            tieneObjeto = Tiene.objects.filter(id_objeto=str(objeto.id),username = username).first() or None
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
            user.save()
            dict_response["OK"] = "True"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)








# Compruebo que la sala exista, que no este llena, y que no este unido a ninguna sala
# class SalaUnir(APIView):
#     #Necesita la autenticazion
#     permission_classes = [IsAuthenticated]
#     @extend_schema(tags=["SALA"],request=SalaUnirRequestSerializer, responses=SalaUnirResponseSerializer)
#     def post(self, request):
#         dict_response = {
#             'OK':"",
#             'error_sala':"",
#         }
#         username, token = get_username_and_token(request)
#         nombre_sala = request.data.get('nombre_sala')
#         password = request.data.get('password')

#         sala = Sala.objects.filter(nombre_sala=nombre_sala).first() or None
#         usuario_instance = Usuario.objects.filter(username=username).first() or None
#         #Check if sala exists
#         if sala:
#             #Check if the user is already in a sala
#             if(not UsuariosSala.objects.filter(username=usuario_instance).exists):
#                 jugadores_en_partida =  UsuariosSala.objects.filter(nombre_sala=nombre_sala).count()
#                 if(jugadores_en_partida > sala.n_jugadores):
#                     any_error = 1
#                     dict_response['error_sala'] = "La sala esta llena, no puedes unirte"
#             else:
#                 any_error = 1
#                 dict_response['error_sala'] = "Ya perteneces a una sala, no puedes unirte"                
#         else:
#             any_error = 1
#             dict_response['error_sala'] = "La sala no existe"
            
#         if any_error ==0:
#             sala_usuario = UsuariosSala.objects.create(nombre_sala=sala,username=usuario_instance,equipo=1)
#             sala_usuario.save()
#             dict_response['OK'] = "True"
#         else:
#             dict_response['OK'] = "False"
#         return Response(dict_response)


# class SalaSalir(APIView):
#     #Necesita la autenticazion
#     permission_classes = [IsAuthenticated]
#     @extend_schema(exclude=True)
#     def post(self, request):
#         any_error = 0
#         dict_response = {
#             'OK':"",
#             'error_sala':"",
#         }
#         username, token = get_username_and_token(request)
#         usuario_instance = Usuario.objects.filter(username=username).first() or None
#         try:
#             UsuariosSala.objects.filter(username=usuario_instance).delete()
#             dict_response['OK'] = "True"
#         except:
#             dict_response['OK'] = "False"
#             dict_response["error_sala"] = "Ya no perteneces a esa sala, no puedes salir"
#         return Response(dict_response)
