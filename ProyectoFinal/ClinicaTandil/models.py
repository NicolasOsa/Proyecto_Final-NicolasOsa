from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    es_paciente = models.BooleanField(default=False)
    es_medico = models.BooleanField(default=False)
    es_secretaria = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

class Paciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return f"{self.usuario.first_name}, {self.usuario.last_name} - {self.usuario.email}"

class Medico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    especialidad = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.usuario.first_name}, {self.usuario.last_name} - {self.usuario.especialidad}"

class Secretaria(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return f"{self.usuario.first_name}, {self.usuario.last_name} - Secretaria/o"

class Mensaje(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.TextField()
    msj_fecha = models.DateTimeField(auto_now_add=True)

class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    turno_fecha = models.DateTimeField()

class Diagnostico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='diagnostico')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    diagnostico = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

class HistoriaClinica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
   