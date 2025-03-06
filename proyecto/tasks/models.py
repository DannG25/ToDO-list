from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """
   Representa una tarea creada por un usuario.

    Atributos:
 user (Usuario): El usuario que ha creado la tarea.
 title (str): El título de la tarea.
 description (str): Una descripción detallada de la tarea.
 start_time (datetime): La hora de inicio de la tarea.
 end_time (datetime): La hora de finalización de la tarea.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return str(self.title)
