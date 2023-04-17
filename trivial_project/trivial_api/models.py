from django.db import models
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Modelos de la base de datos


class Casilla_Tematica(models.Model):
    casilla = models.IntegerField(primary_key = True)
    tematica = models.CharField(max_length = 50, null = False)
    quesito = models.BooleanField(null = False)

    class Meta:
        db_table = "Casilla_Tematica"

class Tablero(models.Model):
    casilla_actual = models.ForeignKey(Casilla_Tematica, on_delete = models.CASCADE, db_column="casilla_actual", related_name='tablero_ac')
    tirada_dado = models.IntegerField(null = False)
    casilla_nueva = models.ForeignKey(Casilla_Tematica, on_delete = models.CASCADE, db_column="casilla_nueva", related_name='tablero_nu')
    
    class Meta:
        db_table = "Tablero"
        unique_together = (("casilla_actual", "casilla_nueva"),)

class Pregunta(models.Model):
    enunciado = models.CharField(max_length = 200, primary_key = True)
    r1 = models.CharField(max_length = 200, blank = True, null = False)
    r2 = models.CharField(max_length = 200, blank = True, null = False)
    r2 = models.CharField(max_length = 200, blank = True, null = False)
    r4 = models.CharField(max_length = 200, blank = True, null = False)
    rc = models.IntegerField(null = False)
    categoria = models.CharField(max_length = 50, null = False)
    
    class Meta:
        db_table = "Pregunta"

class Usuario(AbstractUser):
    username = models.CharField(default="ad",max_length=50, primary_key = True)
    correo = models.EmailField(default="example@gmail.com",blank=False,null=False,unique=True)
    telefono = models.IntegerField(default=0)
    fecha_nac = models.DateField(default="1997-10-19")
    password = models.CharField(default="",max_length=200) #La contraseña cifrada ocupa 128 caracteres
    monedas = models.IntegerField(default=0)


    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    class Meta:
        db_table = "Usuario"

class Amigos(models.Model):
    user1 = models.ForeignKey(Usuario, on_delete = models.CASCADE, db_column = "user1", related_name = 'user1')
    user2 = models.ForeignKey(Usuario, on_delete = models.CASCADE, db_column = "user2", related_name = 'user2')
    
    def clean(self):
        if self.user_id == self.amigo_id:
            raise ValidationError('Username and amigo must be different.')
        
    class Meta:
        #Para indicar que la clave primaria es multiple
        db_table = "Amigos"
        unique_together = (("user1", "user2"),)
    
class Partida(models.Model):
    tipo = models.CharField(max_length = 50, null = False)
    terminada = models.BooleanField(null = False, default = False)
    orden_jugadores = models.CharField(max_length = 100, null = False)
    turno_actual = models.IntegerField(null = False, default = 0)

    class Meta:
        db_table = "Partida"

class Juega(models.Model):
    id_jugador = models.ForeignKey(Usuario, on_delete = models.CASCADE, db_column = "id_jugador", related_name = 'id_jugador')
    id_partida = models.ForeignKey(Partida, on_delete = models.CASCADE, db_column = "id_partida", related_name = 'id_partida')
    posicion = models.IntegerField(null = False, default = 72)
    q_historia = models.BooleanField(null = False, default = False)
    q_arte = models.BooleanField(null = False, default = False)
    q_deporte = models.BooleanField(null = False, default = False)
    q_ciencia = models.BooleanField(null = False, default = False)
    q_entretenimiento = models.BooleanField(null = False, default = False)
    q_geografia = models.BooleanField(null = False, default = False)

    class Meta:
        db_table = "Juega"
        unique_together = (("id_jugador", "id_partida"),)

class Objetos(models.Model):
    objeto = models.AutoField(primary_key = True)
    coste = models.IntegerField(default = 5, null = False)
    link_imagen = models.CharField(max_length = 100)
    tipo = models.CharField(max_length = 7, null = False)

    class Meta:
        db_table = "Objetos"

class Tiene(models.Model):
    id_objeto = models.ForeignKey(Objetos, on_delete = models.CASCADE, db_column = "id_objeto", related_name = 'id_objeto')
    id_usuario = models.ForeignKey(Usuario, on_delete = models.CASCADE, db_column = "id_usuario", related_name = 'id_usuario')

    class Meta:
        db_table = "Tiene"
        unique_together = (("id_objeto", "id_usuario"),)

class Estadisticas(models.Model):
    user_id = models.OneToOneField(Usuario, on_delete=models.CASCADE,db_column = "user_id", related_name = 'estadisticas_username', primary_key = True)
    geografia_bien = models.IntegerField(default = 0)
    geografia_mal = models.IntegerField(default = 0)
    arte_y_literatura_bien = models.IntegerField(default = 0)
    arte_y_literatura_mal = models.IntegerField(default = 0)
    historia_bien = models.IntegerField(default = 0)
    historia_mal = models.IntegerField(default = 0)
    entretenimiento_bien = models.IntegerField(default = 0)
    entretenimiento_mal = models.IntegerField(default = 0)
    ciencias_bien = models.IntegerField(default = 0)
    ciencias_mal = models.IntegerField(default = 0)
    deportes_bien = models.IntegerField(default = 0)
    deportes_mal = models.IntegerField(default = 0)
    quesitos = models.IntegerField(default = 0)
    partidas_ganadas = models.IntegerField(default = 0)
    partidas_perdidas = models.IntegerField(default = 0)

    class Meta:
        db_table = "Estadisticas"


class Sala(models.Model):
    PARTIDA_CHOICES = [
        ('Clasico', 'Clasico'),
        ('Equipo', 'Equipo'),
        ('Tematico', 'Tematico'),
    ]

    SALA_CHOICES = [
        ('Publico', 'Publico'),
        ('Privado', 'Privado'),
    ]
    nombre_sala = models.CharField(max_length=50,primary_key=True)
    creador_id = models.ForeignKey(Usuario,on_delete=models.CASCADE,db_column="creador_id",related_name='creador_sala')
    tiempo_respuesta = models.IntegerField(default=15)
    n_jugadores = models.IntegerField(default=0)
    password_sala = models.CharField(default="",max_length=200) #La contraseña cifrada ocupa 128 caracteres
    tipo_partida = models.CharField(max_length=10,choices=PARTIDA_CHOICES)
    tipo_sala = models.CharField(max_length=10,choices=SALA_CHOICES)

    def set_password(self, raw_password):
        self.password_sala = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_sala)
    
    class Meta:
        db_table = "Sala"


#Guardamos los usuarios de la sala y al equipo que pertenecen
class UsuariosSala(models.Model):
    nombre_sala = models.ForeignKey(Sala,on_delete=models.CASCADE,to_field='nombre_sala',db_column="nombre_sala",related_name='usuarios_sala_usuario_nombre_sala')
    user_id = models.ForeignKey(Usuario,on_delete=models.CASCADE,db_column="user_id",related_name='usuarios_sala_usuario')
    equipo = models.IntegerField(default=1)
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['nombre_sala', 'user_id'], name='usuario_sala_pk')
        ] 
        db_table = "UsuariosSala"