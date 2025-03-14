# pylint: disable=no-member

# 1. Importaciones estándar de Python
from smtplib import SMTPException
import os

# 2. Importaciones de terceros (Django y otras librerías externas)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_delete

# 3. Importaciones locales (tu aplicación)
from .models import Task
from .forms import TaskForm, EmailConfigForm

User = get_user_model()


@login_required
def task_list(request):
    """
    Muestra una lista de tareas pendientes y resueltas para el usuario actual.
    """
    tasks = Task.objects.filter(user=request.user)
    tareas_pendientes = tasks.filter(
        resuelto=False).order_by('-fecha_asignacion')
    tareas_resueltas = tasks.filter(
        resuelto=True).order_by('-fecha_asignacion')

    return render(request, 'tasks/task_list.html', {
        'tareas_pendientes': tareas_pendientes,
        'tareas_resueltas': tareas_resueltas,
    })


@login_required
def task_create(request):
    """
    Maneja la creación de una nueva tarea.
    """
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Tarea creada exitosamente.')
            return redirect('task_list')
        else:
            messages.error(
                request, 'Por favor corrige los errores en el formulario.')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_update(request, pk):
    """
    Maneja la actualización de una tarea existente.
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada exitosamente.')
            return redirect('task_list')
        else:
            messages.error(
                request, 'Por favor corrige los errores en el formulario.')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_update.html', {'form': form})


@login_required
def task_delete(request, pk):
    """
    Gestiona la eliminación de una tarea.
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tarea eliminada exitosamente.')
        return redirect('task_list')
    return render(request, 'tasks/task_delete.html', {'task': task})



@login_required
def check_resolve(request, pk):
    """
    Marca una tarea como resuelta.

    Args:
        request (HttpRequest): La solicitud HTTP.
        pk (int): El ID de la tarea que se marcará como resuelta.
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.resuelto = True  # Marcar la tarea como resuelta
    task.save()
    messages.success(request, 'Tarea marcada como resuelta.')
    return redirect('task_list')


def configure_email(request):
    """
    Configura los detalles del servidor de correo y los almacena en la sesión.
    """
    if request.method == 'POST':
        form = EmailConfigForm(request.POST)
        if form.is_valid():
            email_config = {
                'email_host': form.cleaned_data['email_host'],
                'email_port': form.cleaned_data['email_port'],
                'email_use_tls': form.cleaned_data['email_use_tls'],
                'email_host_user': form.cleaned_data['email_host_user'],
                'email_host_password': form.cleaned_data['email_host_password'],
            }
            request.session['email_config'] = email_config
            messages.success(
                request, 'Configuración de correo guardada exitosamente.')
            return redirect('send_email')
        else:
            messages.error(
                request, 'Por favor corrige los errores en el formulario.')
    else:
        form = EmailConfigForm()
    return render(request, 'email_config.html', {'form': form})


def send_email(request):
    """
    Envía un correo electrónico utilizando la configuración almacenada en la sesión.
    """
    email_settings = request.session.get('email_config', None)
    if not email_settings:
        messages.error(request, 'Configuración de correo no encontrada.')
        return redirect('configure_email')

    try:
        send_mail(
            subject='Restablece tu contraseña ToDo App',
            message='Cuerpo del mensaje.',
            from_email=email_settings['email_host_user'],
            recipient_list=['destinatario@example.com'],
            auth_user=email_settings['email_host_user'],
            auth_password=email_settings['email_host_password'],
            fail_silently=False,
        )
        messages.success(request, 'Correo enviado exitosamente.')
        return render(request, 'email_sent.html')
    except SMTPException as e:
        messages.error(request, f'Error al enviar el correo: {str(e)}')
        return render(request, 'email_error.html', {'error': str(e)})


@receiver(post_delete, sender=Task)
def delete_archivo(sender, instance, **kwargs):
    """
    Elimina el archivo asociado cuando se elimina una tarea.
    """
    if instance.archivo:
        if os.path.isfile(instance.archivo.path):
            os.remove(instance.archivo.path)
