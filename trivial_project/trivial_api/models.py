from django.db import models
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Modelos de la base de datos


class Tematica(models.Model):
    tema = models.CharField(default="NO_ESPECIFICADO",max_length=100,blank=False,null=False, primary_key=True)

    class Meta:
        db_table = "Tematica"


class Pregunta(models.Model):
    enunciado = models.CharField(max_length=200,primary_key=True)
    r_bien = models.CharField(max_length=200,blank=True,null=False)
    r_mal1 = models.CharField(max_length=200,blank=True,null=False)
    r_mal2 = models.CharField(max_length=200,blank=True,null=False)
    r_mal3 = models.CharField(max_length=200,blank=True,null=False)
    tema = models.ForeignKey(Tematica, on_delete=models.CASCADE,default="NO_ESPECIFICADO")
    #Si ponemos esto cambia el nombre de la tabla
    class Meta:
        db_table = "Pregunta"

class Tablero(models.Model):
    casilla_actual = models.IntegerField(max_length = 2,primary_key = True)
    tirada_dado = models.IntegerField(max_length = 2, null = False)
    casilla_nueva = models.IntegerField(max_length = 2, null = False)
    class Meta:
        db_table = "Tablero"

# Tiene un campo que es id, el cual es la clave primaria
class Usuario(AbstractUser):
    username = models.CharField(default="ad",max_length=50, unique=True)
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
    user_id = models.ForeignKey(Usuario, on_delete=models.CASCADE,db_column="user_id", related_name='amigos_username_id')
    amigo_id = models.ForeignKey(Usuario, on_delete=models.CASCADE,db_column="amigo_id",related_name='amigos_amigo_id')
    #pendiente = models.BooleanField()
    #This method will be called by Django Validation Framework before saving the instance to the database
    # and if the username and amigo are the same will raise an exception
    def clean(self):
        if self.user_id == self.amigo_id:
            raise ValidationError('Username and amigo must be different.')
        
    class Meta:
        #Para indicar que la clave primaria es multiple
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'amigo_id'], name='amigos_pk')
        ] 
        db_table = "Amigos"
    

class Partida(models.Model):
    id_partida = models.AutoField(primary_key=True)
    PARTIDA_CHOICES = [
        ('C', 'Clasico'),
        ('E', 'Equipo'),
        ('D', 'Desafio'),
        ('T', 'Tematico'),
    ]
    tipo = models.CharField(max_length=50,choices=PARTIDA_CHOICES) #Para guardar se pone la inicial.

    class Meta:
        db_table = "Partida"


class Historico(models.Model):
    id_partida = models.ForeignKey(Partida, on_delete=models.CASCADE,related_name='historico_id_partida')
    user_id = models.ForeignKey(Usuario,on_delete=models.CASCADE,db_column="user_id",related_name='historico_username')
    he_ganado = models.BooleanField()
    preguntas_respondidas = models.IntegerField(0)
    quesitos = models.IntegerField(0)
    EQUIPO_CHOICES = [
        ('E1', 'Equipo1'),
        ('E2', 'Equipo2'),
        ('E3', 'Equipo3'),
    ]
    equipo = models.CharField(max_length=15,choices=EQUIPO_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_partida', 'user_id'], name='historico_pk')
        ] 
        db_table = "Historico"


class Estadisticas(models.Model):
    user_id = models.ForeignKey(Usuario,on_delete=models.CASCADE,db_column="user_id",related_name='estadisticas_username')
    geografia_bien = models.IntegerField(default=0)
    geografia_mal = models.IntegerField(default=0)
    arte_y_literatura_bien = models.IntegerField(default=0)
    arte_y_literatura_mal = models.IntegerField(default=0)
    historia_bien = models.IntegerField(default=0)
    historia_mal = models.IntegerField(default=0)
    entretenimiento_bien = models.IntegerField(default=0)
    entretenimiento_mal = models.IntegerField(default=0)
    ciencias_bien = models.IntegerField(default=0)
    ciencias_mal = models.IntegerField(default=0)
    deportes_bien = models.IntegerField(default=0)
    deportes_mal = models.IntegerField(default=0)

    class Meta:
        db_table = "Estadisticas"


class Fichas_tableros(models.Model):
    id_objeto = models.AutoField(primary_key=True)
    coste = models.IntegerField(default=5)
    link_imagen = models.CharField(max_length=100)
    TIPO_CHOICES = [
        ('T', 'Tablero'),
        ('F', 'Ficha'),
    ]
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES) #To save you will have to put, 'T' or 'F'

    class Meta:
        db_table = "Fichas_tableros"


class Adquirido(models.Model):
    user_id = models.ForeignKey(Usuario,on_delete=models.CASCADE,db_column="user_id",related_name='adquirido_username')
    id_objeto = models.ForeignKey(Fichas_tableros, on_delete=models.CASCADE,related_name='adquirido_id_objeto')
    adquirido = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'id_objeto'], name='adquirido_pk')
        ] 
        db_table = "Adquirido"



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