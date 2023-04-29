from django.db import models
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Modelos de la base de datos

class Usuario(AbstractUser):
    username = models.CharField(default="ad",max_length=50, primary_key = True)
    correo = models.EmailField(default="example@gmail.com",blank=False,null=False,unique=True)
    telefono = models.IntegerField(default=0)
    fecha_nac = models.DateField(default="1997-10-19")
    password = models.CharField(default="",max_length=200) #La contraseña cifrada ocupa 128 caracteres
    monedas = models.IntegerField(default=0)
    image_perfil = models.CharField(default="/static/images/perfil/default_perfil.png",max_length=200)
    image_tablero = models.CharField(default="/static/images/perfil/default_tablero.png",max_length=200)
    image_ficha = models.CharField(default="/static/images/perfil/default_ficha.png",max_length=200)


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
        constraints = [
        models.UniqueConstraint(fields=['user1', 'user2'], name='usuario_amigo_pk')
        ] 

class Objetos(models.Model):
    TIPO_CHOICES = (
        ('ficha', 'Ficha'),
        ('tablero', 'Tablero'),
    )
    id = models.IntegerField(primary_key = True)
    coste = models.IntegerField(default = 5, null = False)
    tipo = models.CharField(max_length = 7,choices=TIPO_CHOICES, null = False)
    image = models.CharField(max_length=200)

    class Meta:
        db_table = "Objetos"

class Tiene(models.Model):
    id_objeto = models.ForeignKey(Objetos, on_delete = models.CASCADE, db_column = "id_objeto", related_name = 'id_objeto')
    username = models.ForeignKey(Usuario, on_delete = models.CASCADE,related_name="username_objeto")
    enUso = models.IntegerField(default=0)

    class Meta:
        db_table = "Tiene"
        constraints = [
        models.UniqueConstraint(fields=['id_objeto', 'username'], name='usuario_objeto_pk')
        ] 

class Estadisticas(models.Model):
    username = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name = 'estadisticas_username', primary_key = True)
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
