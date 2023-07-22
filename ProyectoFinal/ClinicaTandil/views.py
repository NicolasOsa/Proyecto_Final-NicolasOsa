from django.http import HttpResponse
from django.shortcuts import render,redirect
from ClinicaTandil.models import Mensaje, Avatar, Paciente, Medico
from ClinicaTandil.forms import AvatarForm, UserEditForm, ChangePasswordForm
from .models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def base(request):
    avatar = getavatar(request)
    return render(request, "ClinicaTandil/base.html", {"avatar": avatar})

def home(request):
    return render(request, "ClinicaTandil/home.html")
                  
def turnos(request):
    return render(request, "ClinicaTandil/turnos.html")

def plantilla(request):
    Medicos = Medico.objects.all()
    return render(request, "ClinicaTandil/plantilla.html", {"Medicos": Medicos})

def pacientes(request):
    Pacientes = Paciente.objects.all()
    return render(request, "ClinicaTandil/pacientes.html", {"Pacientes": Pacientes})

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
            return redirect('Home')
    else:
        userCreate = UserCreationForm()
        return render(request, 'ClinicaTandil/registro.html', {'form': userCreate})

@login_required
def perfilview(request):
    return render(request, 'ClinicaTandil/perfil/perfil.html',  {'user': request.user})


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
            return redirect('perfil')
    else:
        form = UserEditForm(initial= {'username': usuario.username, 'email': usuario.email, 'first_name': usuario.first_name, 'last_name': usuario.last_name })
        return render(request, 'ClinicaTandil/perfil/editarPerfil.html', {"form": form})



def crear_avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            user = User.objects.get(username = request.user)
            avatar = Avatar(user = user, imagen = form.cleaned_data['avatar'], id = request.user.id)
            avatar.save()
            avatar = Avatar.objects.filter(user = request.user.id)
            try:
                avatar = avatar[0].imagen.url
            except:
                avatar = None           
            return render(request, "ClinicaTandil/base.html", {'avatar': avatar})
    else:
        try:
            avatar = Avatar.objects.filter(user = request.user.id)
            form = AvatarForm()
        except:
            form = AvatarForm()
    return render(request, "ClinicaTandil/perfil/avatar.html", {'form': form})

def getavatar(request):
    avatar = Avatar.objects.filter(user = request.user.id)
    try:
        avatar = avatar[0].image.url
    except:
        avatar = None
    return avatar


@login_required
def changePassword(request):
    usuario = request.user    
    if request.method == "POST":
        form = ChangePasswordForm(data = request.POST, user = usuario)
        if form.is_valid():
            if request.POST['new_password1'] == request.POST['new_password2']:
                user = form.save()
                update_session_auth_hash(request, user)
            return HttpResponse("Las constraseñas no coinciden")
        return render(request, "ClinicaTandil/base.html")
    else:
        form = ChangePasswordForm(user = usuario)
        return render(request, 'ClinicaTandil/perfil/changePassword.html', {"form": form})



#def crear_avatar(request):
#    if request.method == 'POST':
#        form = AvatarForm(request.POST, request.FILES)
#        if form.is_valid():
#            form.save(request.user)  # Pasamos el usuario actual al formulario
#            return redirect('Home')  # Cambia 'ruta_exitosa' a la URL a la que deseas redirigir después de guardar la información
#    else:
#        form = AvatarForm()
#
#    return render(request, 'ClinicaTandil/perfil/avatar.html', {'form': form})