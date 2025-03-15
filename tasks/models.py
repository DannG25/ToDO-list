from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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
    nota = models.TextField(blank=True, null=True)
    fecha_asignacion = models.DateTimeField(default=timezone.now)
    fecha_vencimiento = models.DateField(
        default=timezone.now)  # Valor predeterminado
    archivo = models.FileField(upload_to='archivos/', blank=True, null=True)
    resuelto = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default='sin_prioridad')


def __str__(self):
    return str(self.title)
