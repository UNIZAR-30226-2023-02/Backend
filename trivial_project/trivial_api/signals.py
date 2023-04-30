from django.db.models.signals import post_migrate
from django.dispatch import receiver
import os
from django.conf import settings

from django.conf.urls.static import static
from trivial_api.models import *
from sala.models import *
from partida.models import *
import trivial_api.models

@receiver(post_migrate)
def populate_data(sender, **kwargs):
    # Solo poblamos una vez, para trivial_api
    sender_name = str(sender).split(':')[1].strip()[:-1]
    if sender_name == "trivial_api":
        try:
            i = 1
            # Solo guardar las de color blanco para que se muestren en la tienda.
            # Fichas 1-9
            while i <= 9:
                image_path = os.path.normpath(os.path.join(settings.STATIC_URL, 'images','objetos', f'{i}.png'))
                image_path = image_path.replace('\\', '/')
                objeto = Objetos.objects.create(id=i,coste=5, tipo='ficha',image = image_path)
                objeto.save()
                i +=1
            # Tableros 10-15
            while i <= 15:
                image_path = os.path.normpath(os.path.join(settings.STATIC_URL, 'images','objetos', f'{i}.png'))
                image_path = image_path.replace('\\', '/')
                
                objeto = Objetos.objects.create(id=i,coste=20, tipo='tablero',image = image_path)
                objeto.save()
                i+=1
        except:
            print("Ya estaba poblada la base de datos")
