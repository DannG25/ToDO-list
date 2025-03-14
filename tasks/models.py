from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete
import os

# from django.db.models.signals import post_save


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('sin_prioridad', 'Sin prioridad'),
        ('muy_baja', 'Muy baja'),
        ('baja', 'Baja'),
        ('alta', 'Alta'),
        ('muy_alta', 'Muy alta'),
        ('urgente', 'Urgente'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    nota = models.TextField(blank=True, null=True)  # Campo de nota
    fecha_asignacion = models.DateTimeField(default=timezone.now)
    fecha_vencimiento = models.DateField(
        default=timezone.now)  # Valor predeterminado
    archivo = models.FileField(upload_to='archivos/', blank=True, null=True)
    resuelto = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default='sin_prioridad')


def __str__(self):
    return str(self.title)

# Señal para eliminar el archivo cuando se elimina una tarea


@receiver(post_delete, sender=Task)
def delete_archivo(sender, instance, **kwargs):
    """
    Elimina el archivo asociado cuando se elimina una tarea.
    """
    if instance.archivo:

        if os.path.isfile(instance.archivo.path):
            os.remove(instance.archivo.path)  # Elimina el archivo

# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     image = models.ImageField(
#         upload_to='profile_images/', default='profile_images/default.png')

#     def __str__(self):
#         # Acceder a username a través de user
#         return f'{self.user} Profile'


# # Señal para crear un perfil automáticamente cuando se crea un usuario
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# # Señal para guardar el perfil automáticamente cuando se guarda el usuario
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     if hasattr(instance, 'profile'):  # Verificar si el perfil existe
#         instance.profile.save()
