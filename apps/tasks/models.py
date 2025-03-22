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
    title = models.CharField(max_length=255)
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


class EmailConfig(models.Model):
    """
    Modelo para almacenar la configuración del servidor de correo.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_host = models.CharField(max_length=255, default="localhost")
    email_port = models.IntegerField(default=1025)
    email_use_tls = models.BooleanField(default=False)
    email_use_ssl = models.BooleanField(default=False)
    email_host_user = models.CharField(max_length=255, blank=True, null=True)
    email_host_password = models.CharField(
        max_length=255, blank=True, null=True)
