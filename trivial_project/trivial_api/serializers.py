from rest_framework import serializers
from trivial_api.models import *
from partida.models import *
from sala.models import *



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
    imagen_perfil = serializers.CharField()
    amigos = serializers.ListField(child=serializers.CharField())

# UsuarioDatosOtroUsuario
class UsuarioDatosOtroUsuarioRequestSerializer(serializers.Serializer):
    username = serializers.CharField()

class UsuarioDatosOtroUsuarioResponseSerializer(serializers.Serializer):
    OK = serializers.CharField()
    username = serializers.CharField()
    correo = serializers.EmailField()
    telefono = serializers.CharField()
    fecha_nac = serializers.DateField()
    monedas = serializers.IntegerField()
    imagen_perfil = serializers.CharField()
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
    amigo = serializers.CharField()
    
    
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
    

# SalaLista
class SalaListaRequestSerializer(serializers.Serializer):
    pass


class SalaListaResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ('nombre_sala', 'creador_username', 'tiempo_respuesta', 'n_jugadores', 'tipo_partida', 'tipo_sala')




# SalaListaJugadores
class DatosUsuarioSala(serializers.Serializer):
    username = serializers.CharField()
    equipo = serializers.CharField()

class SalaListaJugadoresRequestSerializer(serializers.Serializer):
    nombre_sala = serializers.CharField()
      
class SalaListaJugadoresResponseSerializer(serializers.Serializer):
    usuarios = DatosUsuarioSala(many=True)
    



# UsuarioEstadisticasYo
class UsuarioEstadisticasYoRequestSerializer(serializers.Serializer):
    pass

class EstadisticasPreguntaSerializer(serializers.Serializer):
    total = serializers.CharField()
    bien = serializers.CharField()
    mal = serializers.CharField()
    porcentaje = serializers.CharField()

class UsuarioEstadisticasYoResponseSerializer(serializers.Serializer):
    OK = serializers.CharField()
    geografia = EstadisticasPreguntaSerializer()
    arte_y_literatura = EstadisticasPreguntaSerializer()
    historia = EstadisticasPreguntaSerializer()
    entretenimiento = EstadisticasPreguntaSerializer()
    ciencias = EstadisticasPreguntaSerializer()
    deportes = EstadisticasPreguntaSerializer()
    
    quesitos_totales = serializers.CharField()
    total_preguntas = serializers.CharField()
    total_respuestas_correctas = serializers.CharField()
    total_respuestas_incorrectas = serializers.CharField()
    porcentaje_respuestas = serializers.CharField()
    error_usuario = serializers.CharField()


# UsuarioEstadisticas
class UsuarioEstadisticasRequestSerializer(serializers.Serializer):
    username = serializers.CharField()


# TiendaObjetos
class ObjetosSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    coste = serializers.IntegerField()
    #tipo = serializers.CharField()
    enUso = serializers.IntegerField()
    adquirido = serializers.IntegerField()
    imagen = serializers.CharField()


class TiendaObjetosRequestSerializer(serializers.Serializer):
    pass

class TiendaObjetosResponseSerializer(serializers.Serializer):
    fichas = ObjetosSerializer(many=True)
    tableros = ObjetosSerializer(many=True)


# ComprarObjetos
class ComprarObjetoRequestSerializer(serializers.Serializer):
    objeto_id = serializers.CharField()
    
class ComprarObjetoResponseSerializer(serializers.Serializer):
    OK = serializers.CharField()
    error = serializers.CharField()


# UsarObjeto
class UsarObjetoRequestSerializer(serializers.Serializer):
    objeto_id = serializers.CharField()
    
class UsarObjetoResponseSerializer(serializers.Serializer):
    OK = serializers.CharField()
    error = serializers.CharField()