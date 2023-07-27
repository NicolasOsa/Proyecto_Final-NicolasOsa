from ClinicaTandil.models import Mensaje, Avatar, Paciente, Medico, Diagnostico,Turno,Secretaria
from ClinicaTandil.forms import AvatarForm, UserEditForm, ChangePasswordForm, formDiagnostico
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView

from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.shortcuts import get_object_or_404


# Create your views here.

def base(request):
    avatar = getavatar(request)
    es_medico = Medico.objects.filter(usuario=request.user).exists()
    return render(request, "ClinicaTandil/base.html", {"avatar": avatar, "es_medico": es_medico})

def home(request):
    avatar = getavatar(request)
    es_medico = False
    if request.user.is_authenticated:
        es_medico = Medico.objects.filter(usuario=request.user).exists()

    return render(request, "ClinicaTandil/home.html", {"avatar": avatar, "es_medico": es_medico})
                  

def plantilla(request):
    avatar = getavatar(request)
    Medicos = Medico.objects.all()
    return render(request, "ClinicaTandil/plantilla.html", {"Medicos": Medicos, "avatar": avatar})

@login_required
def pacientes(request):
    avatar = getavatar(request)
    es_medico = Medico.objects.filter(usuario=request.user).exists()
    Pacientes = Paciente.objects.all()
    return render(request, "ClinicaTandil/pacientes.html", {"Pacientes": Pacientes, "avatar": avatar, "es_medico": es_medico})

def contacto(request):
    avatar = getavatar(request)
    Mensajes = Mensaje.objects.all()
    if request.method =='POST':
        mensaje = Mensaje(nombre=request.POST["nombre"],apellido=request.POST["apellido"], email=request.POST["email"], mensaje=request.POST["mensaje"])
        mensaje.save()   
        return render(request, "ClinicaTandil/home.html")
    return render(request, "ClinicaTandil/contacto.html", {"avatar": avatar, "Mensajes":Mensajes})


def loginWeb(request):
    if request.method == "POST":
        user = authenticate(username = request.POST['user'], password = request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect("../home", {'mensaje': f"Bienbenido a Clinica Tandil"})
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
            messages.error(request,"Las contraseñas no son validas.")
            return render(request, 'ClinicaTandil/registro.html', {'form': userCreate})
    else:
        userCreate = UserCreationForm()
        return render(request, 'ClinicaTandil/registro.html', {'form': userCreate})

@login_required
def perfilview(request):
    avatar = getavatar(request)
    es_medico = Medico.objects.filter(usuario=request.user).exists()
    return render(request, 'ClinicaTandil/perfil/perfil.html',  {'user': request.user, "avatar": avatar, "es_medico": es_medico})


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


@login_required
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
            return render(request, "ClinicaTandil/home.html", {'avatar': avatar})
    else:
        try:
            avatar = Avatar.objects.filter(user = request.user.id)
            form = AvatarForm()
        except:
            form = AvatarForm()
    return render(request, "ClinicaTandil/perfil/avatar.html", {'form': form})

@login_required
def getavatar(request):
    avatar = Avatar.objects.filter(user = request.user.id)
    try:
        avatar = avatar[0].imagen.url
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
                messages.success(request, "Contraseña cambiada correctamente.")
                return redirect('perfil')
            else:
                messages.error(request, "Las contraseñas no coinciden.")
        else:
            messages.error(request, "Hubo un error al cambiar la contraseña. Por favor, intenta nuevamente.")
    else:
        form = ChangePasswordForm(user = usuario)
    return render(request, 'ClinicaTandil/perfil/changePassword.html', {"form": form})

@login_required
def barnav_medico(request):
    es_medico = False
    if request.user.is_authenticated:
        es_medico = Medico.objects.filter(usuario=request.user).exists()

    return render(request, 'base.html', {'es_medico': es_medico})


@login_required
def diagnostico(request, el_paciente):
    avatar = getavatar(request)
    es_medico = Medico.objects.filter(usuario=request.user).exists()
    el_paciente = get_object_or_404(Paciente, usuario__id=el_paciente)
    Diagnosticos = Diagnostico.objects.filter(paciente = el_paciente)
    return render(request, "ClinicaTandil/diagnostico.html", {"Diagnosticos": Diagnosticos, "avatar": avatar, "es_medico": es_medico, "el_paciente": el_paciente})

@login_required
def agregar_diagnostico(request, el_paciente):
    avatar = getavatar(request)
    es_medico = Medico.objects.filter(usuario=request.user).exists()
    el_paciente = get_object_or_404(Paciente, usuario_id=el_paciente)
    diagnosticos_paciente = Diagnostico.objects.filter(paciente=el_paciente)
    if request.method == 'POST':
        form = formDiagnostico(request.POST)
        if form.is_valid():
            medico_actual = Medico.objects.get(usuario=request.user)
            diagnostico_texto = form.cleaned_data['diagnostico']
            diagnostico = Diagnostico(paciente=el_paciente, medico=medico_actual, diagnostico=diagnostico_texto)
            diagnostico.save()
        
        return redirect('diagnostico', el_paciente=el_paciente.usuario.id)
    else:
        form = formDiagnostico()

    return render(request, "ClinicaTandil/agregar_diagnostico.html", {"Diagnosticos": diagnosticos_paciente, "avatar": avatar,"es_medico": es_medico, "el_paciente": el_paciente, "form": form})


@login_required
def nuevo_turno(request):
    avatar = getavatar(request)
    if request.method == 'POST':
        paciente_id = request.POST.get('paciente')
        medico_id = request.POST.get('medico')
        fecha_hora = request.POST.get('fecha')

        paciente = Paciente.objects.get(usuario_id=paciente_id)
        medico = Medico.objects.get(usuario_id=medico_id)

        turno = Turno.objects.create(paciente=paciente, medico=medico, turno_fecha=fecha_hora)
        messages.success(request, f"Turno asignado para {paciente.usuario.first_name} {paciente.usuario.last_name} con el médico {medico.usuario.first_name} {medico.usuario.last_name} el {fecha_hora}.")

        return redirect('Turnos')

    else:
        Pacientes = Paciente.objects.all()
        Medicos = Medico.objects.all()
        return render(request, 'ClinicaTandil/nuevo_turno.html', {"Pacientes": Pacientes, "Medicos": Medicos, "avatar": avatar})


@login_required
def turnos(request):
    avatar = getavatar(request)
    user = request.user

    es_paciente = Paciente.objects.filter(usuario=user).exists()
    es_medico = Medico.objects.filter(usuario = user).exists()
    es_secretaria = Secretaria.objects.filter(usuario = user).exists()

    if es_secretaria:
        turnos = turnos = Turno.objects.all()
    elif es_medico:
        medico_actual = Medico.objects.get(usuario=user)
        turnos = Turno.objects.filter(medico=medico_actual)
    elif es_paciente:
        paciente_actual = Paciente.objects.get(usuario=user)
        turnos = Turno.objects.filter(paciente=paciente_actual)
    else:
        turnos = []

    return render(request, 'ClinicaTandil/turnos.html', {'turnos': turnos, "avatar": avatar})
    