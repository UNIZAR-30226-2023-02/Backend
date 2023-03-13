from django.urls import path

from .views import *

urlpatterns = [
    path('usuarios/login/', UsuarioLogin.as_view()),
    path('usuarios/register/', UsuarioRegistrar.as_view()),
    
    
    path('usuarios/',UsuarioListView.as_view()),
    path('usuarios/<username>/',UsuarioDetailView.as_view()),
    
]