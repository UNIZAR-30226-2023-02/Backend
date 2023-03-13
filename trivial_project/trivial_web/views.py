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

    if request.method == 'POST':
        any_error = 0
        dict_errors = {
            'error_username': "",
            'error_password': "",
            'error_confirm_password': "",
            'error_fecha_nac': "",
            'error_email': "",
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        fecha_nac = request.POST.get('fecha_nac')
        correo = request.POST.get('email')

        # Comprobamos los posibles errores
        
        if Usuario.objects.filter(username=username).exists():
            # Comprobamos que no exista el usuario
            dict_errors['error_username'] = "El usuario ya existe"

        if password.len() < 8:
            dict_errors['error_password'] = "Contraseña inferior a 8 carácteres"
            any_error = 1
        elif password != confirm_password:
            dict_errors['error_password'] = "Contraseñas diferentes"
            dict_errors['error_confirm_password'] = "Contraseñas diferentes"
            any_error = 1
        
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
        if not re.search(regex,correo):
            dict_errors['error_email'] = "Correo no valido"
            any_error = 1
        elif Usuario.objects.filter(correo=correo).exists():
            dict_errors['error_email'] = "El correo ya esta en uso"
            any_error = 1

        if any_error == 0:
            return render(request, 'trivial_web/login.html')
        else:
            return render(request, 'trivial_web/register.html',dict_errors) 

    if request.method == 'GET':
        return render(request, 'trivial_web/register.html')
