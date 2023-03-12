from django.urls import path

from .views import *

urlpatterns = [
    path('usuarios/',UsuarioListView.as_view()),
    path('usuarios/<username>/',UsuarioDetailView.as_view()),
]