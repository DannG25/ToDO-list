from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'nota', 'fecha_vencimiento', 'archivo']
        widgets = {
            # Usar un input de tipo fecha
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
            # 'nota': forms.DateInput(attrs=())
        }
