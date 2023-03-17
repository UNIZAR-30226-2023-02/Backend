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


# Minuto 57 -> https://www.youtube.com/watch?v=EscHWLV43NQ
class UsuarioListView(APIView):
    def post(self,request,format=None):
        if Usuario.objects.all().exists():
            queryset = Usuario.objects.all()
            serializer = UsuarioSerializer(queryset,many=True)
            return Response({'usuarios': serializer.data})
        else:
            return Response({'error':'No users found'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
  
class UsuarioDetailView(APIView):
    def get(self,request,username,format=None):
        usuario = get_object_or_404(Usuario,username=username)
        serializer = UsuarioSerializer(usuario)
        return Response({'usuario':serializer.data},status=status.HTTP_200_OK)
    

class UsuarioLogin(APIView):
    def post(self, request):
        any_error = 0
        dict_response = {
            'OK':"",
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

        if any_error !=0:
            dict_response['OK'] = "False"
        else:
            dict_response['OK'] = "True"
        
        return Response(dict_response)


class UsuarioRegistrar(APIView):
    def post(self, request):
        any_error = 0
        dict_response = {
            'OK':"",
            'error_username': "",
            'error_password': "",
            'error_confirm_password': "",
            'error_fecha_nac': "",
            'error_email': "",
        }
        username = request.data.get('username')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        fecha_nac = request.data.get('fecha_nac')
        correo = request.data.get('email')

        # Comprobamos los posibles errores
        if Usuario.objects.filter(username=username).exists():
            # Comprobamos que no exista el usuario
            dict_response['error_username'] = "El usuario ya existe"

        if len(password) < 8:
            dict_response['error_password'] = "Contraseña inferior a 8 carácteres"
            any_error = 1
        elif password != confirm_password:
            dict_response['error_password'] = "Contraseñas diferentes"
            dict_response['error_confirm_password'] = "Contraseñas diferentes"
            any_error = 1
        
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
        if not correo:
            dict_response['error_email'] = "Correo no puede estar vacio"
            any_error = 1
        elif not re.search(regex,correo):
            dict_response['error_email'] = "Correo no valido"
            any_error = 1
        elif Usuario.objects.filter(correo=correo).exists():
            dict_response['error_email'] = "El correo ya esta en uso"
            any_error = 1

        # Fecha nacimiento formato
        try:
            datetime.strptime(fecha_nac, '%Y-%m-%d')
        except ValueError:
            dict_response['error_fecha_nac'] = "Formato fecha nacimiento invalido(YY-MM-DD)"

        if any_error !=0:
            dict_response['OK'] = "False"
        else:
            # Creamos el registro en la base de datos
            user = Usuario.objects.create(username=username, correo=correo,fecha_nac=fecha_nac,password=password)
            user.set_password(password)
            user.save()
            dict_response['OK'] = "True"
        return Response(dict_response)

    
class UsuarioDatos(APIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        any_error = 0
        dict_response = {
            'OK':"",
            'username':"",
            'correo': "",
            'fecha_nac': "",
            'monedas': "",
            'amigos':[],
        }
        username = request.GET.get('username')
        # Comprobamos los posibles errores
        if Usuario.objects.filter(username=username).exists():
            user = Usuario.objects.get(username=username)
            amigos = Amigos.objects.filter(username=username)
            dict_response['username'] = user.username
            dict_response['correo'] = user.correo
            dict_response['fecha_nac'] = user.fecha_nac
            dict_response['monedas'] = user.monedas    
            for amigo in amigos:
                dict_response['amigos'].append(amigo.amigo_id)       
            dict_response['OK'] = "True"
        else:
            dict_response['OK'] = "False"
        return Response(dict_response)


class UsuarioAddAmigo(APIView):
    def post(self, request):
        any_error = 0
        dict_response = {
            'OK':"",
            'error':""
        }
        username = request.data.get('username')
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
            amigo_db = Amigos.objects.create(username=usuario_instance,amigo=amigo_instance)
            amigo_db.save()
            dict_response['OK'] = "True"
        else:
            dict_response["OK"] = "False"
        return Response(dict_response)
    


