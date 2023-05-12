from django.urls import path,re_path
from .views import *

# Imagenes
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# API documentation
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView



urlpatterns = [
    # Endpoints para usuarios
    path('usuarios/login/', UsuarioLogin.as_view()),
    path('usuarios/register/', UsuarioRegistrar.as_view()),
    path('usuarios/datos-yo/', UsuarioDatos.as_view()),
    path('usuarios/datos-usuario/', UsuarioDatosOtroUsuario.as_view()),
    path('usuarios/cambiar-datos/', UsuarioCambiarDatos.as_view()),
    path('usuarios/add/amigo/', UsuarioAddAmigo.as_view()),
    path('usuarios/delete/amigo/', UsuarioDeleteAmigo.as_view()),
    path('usuarios/dar-baja/', UsuarioDarDeBaja.as_view()),
    

    path('usuarios/estadisticas-yo/', UsuarioEstadisticasYo.as_view()),
    path('usuarios/estadisticas-usuario/',UsuarioEstadisticasOtroUsuario.as_view()),

    # Endpoints para las salas
    path('salas/crear/', SalaCrear.as_view()),
    path('salas/validar/', SalaValidarUnir.as_view()),
    path('salas/lista-salas/', SalaLista.as_view()),
    path('salas/lista-jugadores-sala/', SalaListaJugadores.as_view()),
    path('salas/enviar-peticion/', EnviarPeticionUnirSala.as_view()),
    path('salas/listar-peticiones-sala/', ListarPeticionesSala.as_view()),
    
    # Endpoints ADMIN
    path('admin/login/', AdminLogin.as_view()),
    path('admin/preguntas/delete/', EliminarPregunta.as_view()),
    path('admin/preguntas/add/', AddPregunta.as_view()),
    path('admin/preguntas/edit/', EditPregunta.as_view()),
    path('admin/preguntas/info/', InfoPregunta.as_view()),
    path('admin/preguntas/lista/', ListarPreguntas.as_view()),
    path('admin/monedas-infinitas/', ListarPreguntas.as_view()),

        # Uno con todas las fotos de perfil disponibles

    # Endpoints para la tienda
    path('tienda/objetos/', TiendaObjetos.as_view()),
    path('tienda/comprar/', ComprarObjeto.as_view()),
    path('tienda/usar/', UsarObjeto.as_view()),
    
    #Endpoints para las partidas
    path('partidas/activas/', PartidaActiva.as_view()),

    # Endpoints para la documentacion
    path('documentacion/', SpectacularSwaggerView.as_view(url_name='documentacion')),
    path('documentacion/swagger-ui', SpectacularAPIView.as_view(), name='documentacion'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='documentacion'), name='redoc'),
]

# Para permitir acceder a imagenes
urlpatterns += staticfiles_urlpatterns() 