from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

import re
from datetime import datetime




# Minuto 57 -> https://www.youtube.com/watch?v=EscHWLV43NQ
class UsuarioListView(APIView):
    def get(self,request,format=None):
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
            'validate':"",
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
            dict_response['validate'] = "False"
        else:
            dict_response['validate'] = "True"
        
        return Response(dict_response)



class UsuarioRegistrar(APIView):
    def post(self, request):
        any_error = 0
        dict_response = {
            'created':"",
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
            dict_response['created'] = "False"
        else:
            # Creamos el registro en la base de datos
            user = Usuario.objects.create(username=username, correo=correo,fecha_nac=fecha_nac,password=password)
            user.set_password(password)
            user.save()
            dict_response['created'] = "True"
        return Response(dict_response)