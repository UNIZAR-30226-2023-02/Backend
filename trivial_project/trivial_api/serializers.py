from rest_framework import serializers
from .models import *
from datetime import datetime
import re
#Token
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from trivial_api.funciones_auxiliares import *



# UsuarioLogin
class UsuarioLoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UsuarioLoginResponseSerializer(serializers.Serializer):
    OK = serializers.CharField()
    token = serializers.CharField()
    error_username = serializers.CharField()
    error_password = serializers.CharField()

# UsuarioRegistrar
class UsuarioRegistrarRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    fecha_nac = serializers.DateField()
    correo = serializers.EmailField()
    telefono = serializers.IntegerField()

class UsuarioRegistrarResponseSerializer(serializers.Serializer):
    OK = serializers.CharField()
    token = serializers.CharField()
    error_username = serializers.CharField()
    error_password = serializers.CharField()
    error_confirm_password = serializers.CharField()
    error_fecha_nac = serializers.CharField()
    error_correo = serializers.CharField()
    error_telefono = serializers.CharField()

# UsuarioDatos
class UsuarioDatosRequestSerializer(serializers.Serializer):
    pass

class UsuarioDatosResponseSerializer(serializers.Serializer):
    OK = serializers.CharField()
    username = serializers.CharField()
    correo = serializers.EmailField()
    telefono = serializers.CharField()
    fecha_nac = serializers.DateField()
    monedas = serializers.IntegerField()
    imagen = serializers.ImageField()
    amigos = serializers.ListField(child=serializers.CharField())

# UsuarioCambiarDatos
class UsuarioCambiarDatosRequestSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    telefono = serializers.IntegerField()
    fecha_nac = serializers.DateField()
    

class UsuarioCambiarDatosResponseSerializer(serializers.Serializer):
    OK = serializers.CharField()
    error_correo = serializers.CharField()
    error_fecha_nac = serializers.CharField()
    error_telefono = serializers.CharField()


# UsuarioAddAmigo
class UsuarioAddAmigoRequestSerializer(serializers.Serializer):
    amigo_username = serializers.CharField()
    
    
class UsuarioAddAmigoResponseSerializer(serializers.Serializer):
    OK = serializers.CharField()
    error = serializers.CharField()
    
# SalaCrear
class SalaCrearRequestSerializer(serializers.Serializer):
    nombre_sala = serializers.CharField()
    tiempo_respuesta = serializers.IntegerField()
    password_sala = serializers.CharField()
    n_jugadores = serializers.IntegerField()
    tipo_partida = serializers.CharField()
    
    
class SalaCrearResponseSerializer(serializers.Serializer):
    OK = serializers.CharField()
    error_nombre_sala = serializers.CharField()
    error_tipo_sala = serializers.CharField()
    error_tipo_partida = serializers.CharField()
    error_n_jugadores = serializers.CharField()
    error_tiempo_respuesta = serializers.CharField()

# SalaUnir
class SalaUnirRequestSerializer(serializers.Serializer):
    nombre_sala = serializers.CharField()
    
    
    
class SalaUnirResponseSerializer(serializers.Serializer):
    OK = serializers.CharField()
    error_sala = serializers.CharField()
    



#Serializador de la sala
class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ('nombre_sala', 'creador_username', 'tiempo_respuesta', 'n_jugadores', 'tipo_partida', 'tipo_sala')


