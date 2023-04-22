from django.shortcuts import render
from trivial_api.models import *
# Create your views here.



def index(request):
    return render(request, "sala/index.html")


def room(request, room_name):
    return render(request, "sala/room.html", {"room_name": room_name})

def game(request, game_name):
    return render(request, "sala/game.html", {"game_name": game_name})

def lobby(request,room_name):
    return render(request, 'sala/lobby.html',{'room_name': room_name})

def prueba_imagenes(request,objeto_id):
    objeto = Objetos.objects.get(pk=objeto_id)
    return render(request, 'sala/detalle_objeto.html', {'objeto': objeto})