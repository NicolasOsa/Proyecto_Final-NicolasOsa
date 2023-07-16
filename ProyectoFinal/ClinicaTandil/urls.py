from django.urls import path
from django.contrib.auth.views import LogoutView
from ClinicaTandil.views import base, home, turnos, plantilla, pacientes, contacto, loginWeb, registro, perfilview, editarPerfil, crear_avatar

urlpatterns = [
    path('', home, name="Home"),
    path('base/', base),
    path('home/', home, name="Home"),
    path('turnos/', turnos, name="Turnos"),
    path('plantilla/', plantilla, name="Plantilla"),
    path('pacientes/', pacientes, name="Pacientes"),
    path('contacto/', contacto, name="Contacto"),
    path('login/', loginWeb, name="login"),
    path('registro/', registro, name="registro"),
    path('Logout/',LogoutView.as_view(template_name = 'ClinicaTandil/Logout.html'), name="Logout"),
    path('perfil/', perfilview, name="perfil"),
    path('perfil/editarPerfil/', editarPerfil, name="editarPerfil"),
    path('perfil/avatar/', crear_avatar, name="crear_avatar"),
]