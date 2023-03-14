from django.shortcuts import render

# Create your views here.

def lobby(request,room_name):
    return render(request, 'sala/lobby.html',{'room_name': room_name})