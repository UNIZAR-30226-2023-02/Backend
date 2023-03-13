from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from trivial_web.models import *
from django.shortcuts import redirect



def home(request):
    # Redirect to the 'posts' page if no path is specified
    return redirect('trivial_web/index.html')

def index(request):
    return render(request, 'trivial_web/index.html')

#Gestiona el login
def login(request):
    if request.method == 'GET':
        return render(request, 'trivial_web/login.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'trivial_web/register.html')
