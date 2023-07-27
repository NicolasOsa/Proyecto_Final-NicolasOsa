from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Paciente

@receiver(post_save, sender=User)
def create_paciente(sender, instance, created, **kwargs):
    if created:
        Paciente.objects.create(usuario=instance)