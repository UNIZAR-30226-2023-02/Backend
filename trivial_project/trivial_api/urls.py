from django.urls import path,re_path
from rest_framework.authtoken import views
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('usuarios/login/', UsuarioLogin.as_view()),
    path('usuarios/register/', UsuarioRegistrar.as_view()),
     path('usuarios/lista/', UsuarioListView.as_view()),
    # Posible problema, que un usuarios que no sea el vea o agrege amigos a otros usuarios
    path('usuarios/datos/', UsuarioDatos.as_view()),
    path('usuarios/add/amigo', UsuarioAddAmigo.as_view()),

    #path('salas/crear/', UsuarioDatos.as_view()),
     
    #path('usuarios/eliminar/', .as_view()),
    
    path('usuarios/',UsuarioListView.as_view()),
    path('usuarios/<username>/',UsuarioDetailView.as_view()),

    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

    