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


class EmailConfigForm(forms.Form):
    email_host = forms.CharField(label="Servidor SMTP", max_length=100)
    email_port = forms.IntegerField(label="Puerto SMTP")
    email_use_tls = forms.BooleanField(label="Usar TLS", required=False)
    email_host_user = forms.EmailField(label="Correo electrónico")
    email_host_password = forms.CharField(
        label="Contraseña", widget=forms.PasswordInput)
