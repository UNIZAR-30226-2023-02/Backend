from django.db import models

# Modelos de la base de datos

class Pregunta(models.Model):
    enunciado = models.CharField(max_length=500)
    respuesta_correcta = models.CharField(max_length=500)
    respuesta_incorrecta1 = models.CharField(max_length=500)
    respuesta_incorrecta2 = models.CharField(max_length=500)
    respuesta_incorrecta3 = models.CharField(max_length=500)
    #Si ponemos esto cambia el nombre de la tabla
    class Meta:
        db_table = "Pregunta"

class Usuario(models.Model):
    username = models.CharField(max_length=100, primary_key=True)

# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)