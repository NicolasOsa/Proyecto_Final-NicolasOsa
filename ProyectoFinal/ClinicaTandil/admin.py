from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Secretaria)
admin.site.register(Mensaje)
admin.site.register(Turno)
admin.site.register(Diagnostico)