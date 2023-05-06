from django.db import models
from trivial_api.models import *



class Casilla_Tematica(models.Model):
    casilla = models.IntegerField(primary_key = True)
    tematica = models.CharField(max_length = 50, null = False)
    quesito = models.BooleanField(null = False)

    class Meta:
        db_table = "Casilla_Tematica"

# Modelo que calcula las posibles posiciones del jugador dada la tirada
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
    r3 = models.CharField(max_length = 200, blank = True, null = False)
    r4 = models.CharField(max_length = 200, blank = True, null = False)
    rc = models.IntegerField(null = False)
    categoria = models.CharField(max_length = 50, null = False)
    
    class Meta:
        db_table = "Pregunta"


class Partida(models.Model):
    tipo = models.CharField(max_length = 50, null = False)
    terminada = models.BooleanField(null = False, default = False)
    orden_jugadores = models.CharField(max_length = 100, null = False)
    turno_actual = models.IntegerField(null = False, default = 0)

    class Meta:
        db_table = "Partida"

# Información que necesita el jugador dentro de la partida
class Juega(models.Model):
    username = models.ForeignKey(Usuario, on_delete = models.CASCADE)
    id_partida = models.ForeignKey(Partida, on_delete = models.CASCADE, db_column = "id_partida", related_name = 'id_partida')
    # Posicion del jugador
    posicion = models.IntegerField(null = False, default = 72)
    # Quesitos 
    q_historia = models.BooleanField(null = False, default = False)
    q_arte = models.BooleanField(null = False, default = False)
    q_deporte = models.BooleanField(null = False, default = False)
    q_ciencia = models.BooleanField(null = False, default = False)
    q_entretenimiento = models.BooleanField(null = False, default = False)
    q_geografia = models.BooleanField(null = False, default = False)

    #NUEVO
    # Imagen de la ficha en partida
    image = models.CharField(max_length=200)
    activo = models.BooleanField(null = False, default = True) # Para saber si el jugador se ha desconectado
    
    class Meta:
        db_table = "Juega"
        constraints = [
            models.UniqueConstraint(fields=['username', 'id_partida'], name='usuario_partida_pk')
        ] 
