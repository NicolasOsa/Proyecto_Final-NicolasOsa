from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatars/', null=True, blank=True)

class Paciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return f"{self.usuario.first_name}, {self.usuario.last_name} - {self.usuario.email}"

class Medico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    especialidad = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.usuario.first_name}, {self.usuario.last_name} - {self.especialidad}"

class Secretaria(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return f"{self.usuario.first_name}, {self.usuario.last_name} - Secretaria/o"

class Mensaje(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField()
    mensaje = models.TextField()
    msj_fecha = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.nombre}, {self.apellido} - {self.mensaje}"

class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    turno_fecha = models.DateTimeField()
    def __str__(self):
        return f"{self.turno_fecha} - {self.paciente.usuario.last_name}, {self.paciente.usuario.first_name}"

class Diagnostico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='diagnostico')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    diagnostico = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.paciente.usuario.first_name}, {self.paciente.usuario.last_name} - {self.fecha}"



