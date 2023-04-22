from django.urls import path,re_path
from .views import *
from rest_framework import permissions
# To get 
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# API documentation
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
urlpatterns = [
    path('poblar_base/', PoblarBaseDatos.as_view()),

    # Endpoints para usuarios
    path('usuarios/login/', UsuarioLogin.as_view()),
    path('usuarios/register/', UsuarioRegistrar.as_view()),
    path('usuarios/datos/', UsuarioDatos.as_view()),
    path('usuarios/cambiar-datos/', UsuarioCambiarDatos.as_view()),
    path('usuarios/add/amigo/', UsuarioAddAmigo.as_view()),

    #Endpoints para las salas
    path('salas/crear/', SalaCrear.as_view()),
    path('salas/unir/', SalaUnir.as_view()),
    path('salas/salir/', SalaSalir.as_view()),
    path('salas/lista-salas/', SalaLista.as_view()),
    path('salas/lista-jugadores-sala/', SalaListaJugadoresSala.as_view()),

    #Endpoints para las partidas
    #path('partidas/empezar/', Partida.as_view()),


    
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] 

# Para permitir acceder a imagenes
urlpatterns += staticfiles_urlpatterns() 