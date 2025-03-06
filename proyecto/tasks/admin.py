from django.contrib import admin
from .models import Task  # Importa el modelo Task

# Registra el modelo Task en el panel de administración


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):  # Campos que se mostrarán en la lista de tareas
    list_display = ('title', 'user', 'start_time', 'end_time')
    # Filtros para la lista de tareas
    list_filter = ('user', 'start_time', 'end_time')
    # Campos por los que se puede buscar
    search_fields = ('title', 'description')
    # Ordenar las tareas por fecha de inicio (más recientes primero)
    ordering = ('-start_time',)
