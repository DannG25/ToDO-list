from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'nota', 'fecha_vencimiento',
                    'archivo')  # Campos a mostrar en la lista
    list_filter = ('fecha_vencimiento',)  # Campos para filtrar
    search_fields = ('title', 'nota')  # Campos para buscar
    ordering = ('fecha_vencimiento',)  # Ordenar por fecha de vencimiento
