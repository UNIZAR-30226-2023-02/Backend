from django.urls import path,re_path
from rest_framework.authtoken import views
from .views import *
from rest_framework import permissions



urlpatterns = [
    #path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('usuarios/login/', UsuarioLogin.as_view()),
    path('usuarios/register/', UsuarioRegistrar.as_view()),
    # Posible problema, que un usuarios que no sea el vea o agrege amigos a otros usuarios
    path('usuarios/datos/', UsuarioDatos.as_view()),
    path('usuarios/add/amigo', UsuarioAddAmigo.as_view()),

    #path('salas/crear/', UsuarioDatos.as_view()),
     
    #path('usuarios/eliminar/', .as_view()),
    


    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

    