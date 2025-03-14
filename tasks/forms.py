"""
Módulo forms.py

Este módulo define los formularios utilizados en la aplicación, incluyendo:
- Formularios para la creación y actualización de tareas (TaskForm).
- Formularios para la configuración del servidor de correo electrónico (EmailConfigForm).
- Formularios personalizados de autenticación (EmailAuthenticationForm).
- Formularios para la creación y actualización de usuarios
(CustomUserCreationForm, UserEditForm, UserUpdateForm).
- Formularios para la actualización del perfil de usuario (ProfileUpdateForm).
"""

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django import forms
from .models import Task
# from .models import Profile


class TaskForm(forms.ModelForm):
    """
    Formulario para crear o actualizar una tarea.
    Incluye campos para el título, nota, fecha de vencimiento y archivo adjunto.
    """
    class Meta:
        model = Task
        fields = ['title', 'nota', 'fecha_vencimiento', 'archivo', 'priority']
        widgets = {
            # Usar un input de tipo fecha
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }


def clean_archivo(self):
    archivo = self.cleaned_data.get('archivo')
    if archivo:
        # Limitar el tamaño del archivo a 100MB
        if archivo.size > 100 * 1024 * 1024:
            raise ValidationError("El archivo no puede ser mayor a 100MB.")
        # Validar tipos de archivo permitidos
        allowed_types = ['application/pdf', 'application/msword',
                         'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if archivo.content_type not in allowed_types:
            raise ValidationError("Solo se permiten archivos PDF o DOCX.")
    return archivo


class EmailConfigForm(forms.Form):
    """
    Formulario para configurar los detalles del servidor de correo electrónico.
    Incluye campos para el servidor SMTP, puerto, TLS, correo electrónico y contraseña.
    """
    email_host = forms.CharField(label="Servidor SMTP", max_length=100)
    email_port = forms.IntegerField(label="Puerto SMTP")
    email_use_tls = forms.BooleanField(label="Usar TLS", required=False)
    email_host_user = forms.EmailField(label="Correo electrónico")
    email_host_password = forms.CharField(
        label="Contraseña", widget=forms.PasswordInput)


class EmailAuthenticationForm(AuthenticationForm):
    """
    Formulario de autenticación personalizado que permite el inicio de sesión
    con un correo electrónico o nombre de usuario.
    """
    username = forms.CharField(label="Correo electrónico o nombre de usuario")


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario personalizado para la creación de usuarios.
    Incluye campos para el nombre de usuario, correo electrónico y contraseñas.
    """
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# class UserEditForm(forms.ModelForm):
#     """
#     Formulario para editar el nombre de usuario y el correo electrónico de un usuario.
#     """
#     class Meta:
#         model = User
#         fields = ['username', 'email']


# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email']


# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image']
