from django.shortcuts import render

# Create your views here.



def index(request):
    return render(request, "sala/index.html")


def room(request, room_name):
    return render(request, "sala/room.html", {"room_name": room_name})

def game(request, game_name):
    return render(request, "sala/game.html", {"game_name": game_name})

def lobby(request,room_name):
    return render(request, 'sala/lobby.html',{'room_name': room_name})