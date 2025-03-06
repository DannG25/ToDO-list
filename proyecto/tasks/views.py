from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Task
from .forms import TaskForm


def register(request):
    """
    Gestiona el registro de usuarios.

    Si el método de solicitud es POST, procesa el formulario de registro,
    crea un nuevo usuario, lo registra y redirige a la página de inicio de sesión.
    Si el método de solicitud es GET, muestra el formulario de registro.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, '¡Registro exitoso! Por favor inicia sesión.')
            return redirect('task_list')  # Redirige a la lista de tareas
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    """
    Gestiona el inicio de sesión del usuario.

    Si el método de solicitud es POST, autentica al usuario y lo registra
    si las credenciales son válidas.
    Redirige a la página de la lista de tareas si el inicio de sesión se realiza correctamente.
    Si el método de solicitud es GET, muestra el formulario de inicio de sesión.
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
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def task_list(request):
    """
    Muestra una lista de tareas para el usuario actualmente conectado.

    Sólo accesible para usuarios autenticados.
    """
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    """
    Maneja la creación de una nueva tarea.

    Si el método de solicitud es POST, procesa los datos del formulario,
    asocia la tarea al usuario actual y la guarda en la base de datos.
    Si el método de solicitud es GET, muestra el formulario de creación de tarea.
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
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

    Si el método de solicitud es POST, procesa los datos del formulario y actualiza
    la tarea en la base de datos.
    Si el método de solicitud es GET, muestra el formulario de actualización de la tarea.
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada exitosamente.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
    """
    Gestiona la eliminación de una tarea.

    Si el método de solicitud es POST, elimina la tarea de la base de datos.
    Si el método de solicitud es GET, muestra la página de confirmación
    de la eliminación de la tarea.
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Tarea eliminada exitosamente.')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
