from django.urls import path 
from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("imagen/<int:objeto_id>/", views.prueba_imagenes, name="imagen_prueba"),
]


