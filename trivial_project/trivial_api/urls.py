from django.urls import path,re_path
from .views import *
from rest_framework import permissions



urlpatterns = [

    # Endpoints para usuarios
    path('usuarios/login/', UsuarioLogin.as_view()),
    path('usuarios/register/', UsuarioRegistrar.as_view()),
    path('usuarios/datos/', UsuarioDatos.as_view()),
    path('usuarios/add/amigo/', UsuarioAddAmigo.as_view()),

    #Endpoints para las salas
    path('salas/crear/', SalaCrear.as_view()),
    path('salas/unir/', SalaUnirse.as_view()),
    path('salas/lista-salas/', SalaLista.as_view()),
    path('salas/lista-jugadores-sala/', SalaListaJugadoresSala.as_view()),

    #Endpoints para las partidas
    path('partidas/empezar/', SalaUnirse.as_view()),


    


    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

    