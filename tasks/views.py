# 1. Importaciones estándar de Python
from smtplib import SMTPException

# 2. Importaciones de terceros (Django y otras librerías externas)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

# 3. Importaciones locales (tu aplicación)
from .models import Task
from .forms import TaskForm, EmailConfigForm

User = get_user_model()


def register(request):
    """
    Gestiona el registro de usuarios.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, '¡Registro exitoso! Por favor inicia sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    """
    Gestiona el inicio de sesión del usuario.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def task_list(request):
    """
    Muestra una lista de tareas pendientes y resueltas para el usuario actual.
    """
    tasks = Task.objects.filter(user=request.user)
    tareas_pendientes = tasks.filter(resuelto=False)
    tareas_resueltas = tasks.filter(resuelto=True)

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
        form = EmailConfigForm()
    return render(request, 'email_config.html', {'form': form})


def send_email(request):
    """
    Envía un correo electrónico utilizando la configuración almacenada en la sesión.
    """
    email_settings = request.session.get(
        'email_config', None)  # Se usa el nuevo nombre
    if not email_settings:
        return redirect('configure_email')

    try:
        send_mail(
            subject='Asunto del correo',
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
