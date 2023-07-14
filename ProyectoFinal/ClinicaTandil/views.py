from django.shortcuts import render,redirect
from ClinicaTandil.models import Mensaje
from ClinicaTandil.forms import AvatarForm, UserEditForm
from django.contrib.auth.models import AbstractUser
from .models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()

# Create your views here.

def base(request):
    #avatar = getavatar(request)
    return render(request, "ClinicaTandil/base.html")

def home(request):
    return render(request, "ClinicaTandil/home.html")
                  
def turnos(request):
    return render(request, "ClinicaTandil/turnos.html")

def plantilla(request):
    return render(request, "ClinicaTandil/plantilla.html")

def pacientes(request):
    return render(request, "ClinicaTandil/pacientes.html")

def contacto(request):
    if request.method =='POST':
        mensaje = Mensaje(nombre=request.POST["nombre"],apellido=request.POST["apellido"], email=request.POST["email"], mensaje=request.POST["mensaje"])
        mensaje.save()   
        return render(request, "ClinicaTandil/home.html")

    return render(request, "ClinicaTandil/contacto.html")


def loginWeb(request):
    if request.method == "POST":
        
        user = authenticate(username = request.POST['user'], password = request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect("../home", {'mensaje': f"Bienbenido che"})
        else:
            return render(request, 'ClinicaTandil/login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'ClinicaTandil/login.html', {'error': 'Usuario o contraseña incorrectos'})

def registro(request):
    if request.method == "POST":
        userCreate = UserCreationForm(request.POST)
        if userCreate.is_valid():
            user = userCreate.save()
            login(request, user)
            return render(request, 'ClinicaTandil/login.html')
    else:
        userCreate = UserCreationForm()
        return render(request, 'ClinicaTandil/registro.html', {'form': userCreate})

@login_required
def perfilview(request):
    return render(request, 'ClinicaTandil/perfil/perfil.html')


@login_required  
def editarPerfil(request):
    usuario = request.user
    user_basic_info = User.objects.get(id = usuario.id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance = usuario)
        if form.is_valid():
            user_basic_info.username = form.cleaned_data.get('username')
            user_basic_info.email = form.cleaned_data.get('email')
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')
            user_basic_info.save()
            return render(request, 'ClinicaTandil/perfil/perfil.html')
    else:
        form = UserEditForm(initial= {'username': usuario.username, 'email': usuario.email, 'first_name': usuario.first_name, 'last_name': usuario.last_name })
        return render(request, 'ClinicaTandil/perfil/perfil.html', {"form": form})


#def editAvatar(request):
#    if request.method == 'POST':
#        form = AvatarForm(request.POST, request.FILES)
#        print(form)
#        print(form.is_valid())
#        if form.is_valid():
#            user = request.user
#            user.avatar = form.cleaned_data['avatar']
#            user.save()
#            avatar = user.avatar.url
#            try:
#                avatar = avatar[0].image.url
#            except:
#                avatar = None           
#            return render(request, 'ClinicaTandil/home.html', {'avatar': avatar})
#    else:
#        try:
#            form = AvatarForm()
#        except:
#            form = AvatarForm()
#    return render(request, 'ClinicaTandil/home.html', {'form': form})
#
#def getavatar(request):
#    avatar = avatar.objects.filter(user = request.user.id)
#    try:
#        avatar = avatar[0].image.url
#    except:
#        avatar = None
#    return avatar