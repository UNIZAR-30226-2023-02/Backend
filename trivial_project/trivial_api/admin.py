from django.contrib import admin
from .models import Usuario
from .models import Objetos

# Todos los modelos que se registren apareceran en la pagina del admin
admin.site.register(Usuario)
admin.site.register(Objetos)
# Register your models here.
