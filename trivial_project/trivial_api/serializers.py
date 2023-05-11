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


# UsuarioDeleteAmigo
class UsuarioDeleteAmigoRequestSerializer(serializers.Serializer):
    amigo = serializers.CharField()
    
    
class UsuarioDeleteAmigoResponseSerializer(serializers.Serializer):
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
    monedas = serializers.CharField()


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



# PartidaActiva
class partida_wsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    tipo = serializers.CharField()
    #tipo = serializers.CharField()
    ws = serializers.CharField()

class PartidaActivaRequestSerializer(serializers.Serializer):
    id_partida = serializers.CharField()

class PartidaActivaResponseSerializer(serializers.Serializer):
    OK = serializers.CharField()
    partida = partida_wsSerializer(many=True)
    error = serializers.CharField()


# Usuario Dar de baja
class UsuarioDarBajaRequestSerializer(serializers.Serializer):
    pass

class UsuarioDarBajaResponseSerializer(serializers.Serializer):
    pass

# EliminarPregunta
class EliminarPregunta1(serializers.Serializer):
    id = serializers.IntegerField()

class EliminarPregunta2(serializers.Serializer):
    OK = serializers.CharField()
    error = serializers.CharField()


# AddPregunta
class AddPregunta1(serializers.Serializer):
    enunciado = serializers.CharField()
    r1 = serializers.CharField()
    r2 = serializers.CharField()
    r3 = serializers.CharField()
    r4 = serializers.CharField()
    rc = serializers.IntegerField()
    categoria = serializers.CharField()

class AddPregunta2(serializers.Serializer):
    OK = serializers.CharField()
    error = serializers.CharField()


# EditPregunta
class EditPregunta1(serializers.Serializer):
    id = serializers.IntegerField()
    enunciado = serializers.CharField()
    r1 = serializers.CharField()
    r2 = serializers.CharField()
    r3 = serializers.CharField()
    r4 = serializers.CharField()
    rc = serializers.IntegerField()
    categoria = serializers.CharField()

class EditPregunta2(serializers.Serializer):
    OK = serializers.CharField()
    error = serializers.CharField()

# InforPregunta
class InfoPregunta1(serializers.Serializer):
    id = serializers.IntegerField()

class InfoPregunta2(serializers.Serializer):
    OK = serializers.CharField()
    enunciado = serializers.CharField()
    r1 = serializers.CharField()
    r2 = serializers.CharField()
    r3 = serializers.CharField()
    r4 = serializers.CharField()
    rc = serializers.IntegerField()
    categoria = serializers.CharField()
    error = serializers.CharField()


# ListarPreguntas
class enunIDPregunta(serializers.Serializer):
    enunciado = serializers.CharField()
    id = serializers.IntegerField()

class ListarPreguntas1(serializers.Serializer):
    pass

class ListarPreguntas2(serializers.Serializer):
    OK = serializers.CharField()
    preguntas = enunIDPregunta(many=True)


# UsuarioLoginAdmin
class AdminLogin1(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AdminLogin2(serializers.Serializer):
    OK = serializers.CharField()
    token = serializers.CharField()
    error_username = serializers.CharField()
    error_password = serializers.CharField()



# UsuarioLoginAdmin
class AdminLogin1(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AdminLogin2(serializers.Serializer):
    OK = serializers.CharField()
    token = serializers.CharField()
    error_username = serializers.CharField()
    error_password = serializers.CharField()



# EnviarPeticionUnirSala
class EnviarPeticionUnirSala1(serializers.Serializer):
    username_amigo = serializers.CharField()

class EnviarPeticionUnirSala2(serializers.Serializer):
    OK = serializers.CharField()
    error = serializers.CharField()


# EnviarPeticionUnirSala
class peticiones_info(serializers.Serializer):
    me_invita = serializers.CharField()
    ws = serializers.CharField()

class ListarPeticionesSala1(serializers.Serializer):
    pass

class ListarPeticionesSala2(serializers.Serializer):
    OK = serializers.CharField()
    peticiones = peticiones_info(many=True)