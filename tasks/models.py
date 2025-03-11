from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    nota = models.TextField(blank=True, null=True)  # Campo de nota
    fecha_asignacion = models.DateTimeField(default=timezone.now)
    fecha_vencimiento = models.DateField(default=timezone.now)  # Valor predeterminado
    archivo = models.FileField(upload_to='archivos/', blank=True, null=True)
    resuelto = models.BooleanField(default=False)  # Nuevo campo

    def __str__(self):
        return str(self.title)
