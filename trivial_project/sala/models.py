from django.db import models
from trivial_api.models import *
from django.contrib.auth.hashers import make_password,check_password


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
    creador_username = models.ForeignKey(Usuario,on_delete=models.CASCADE,db_column="creador_username",related_name='creador_sala')
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
    nombre_sala = models.ForeignKey(Sala,on_delete=models.CASCADE,db_column="nombre_sala",related_name='usuarios_sala_usuario_nombre_sala')
    username = models.ForeignKey(Usuario,on_delete=models.CASCADE,db_column="username",related_name='usuarios_sala_usuario')
    equipo = models.IntegerField(default=1)
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['nombre_sala', 'username'], name='usuario_sala_pk')
        ] 
        db_table = "UsuariosSala"