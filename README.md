
Novedades y necesidades del código

El proyecto esta en estado 200 (funcional) los siguientes requerimientos son los siguientes:

se necesita agregarle estilos mediante Bootstrap a los archivos para que luzca mas formal y en caso tal no funcione agregarle estilos. /

agregarle readme

Vistas personalizables con condiciones propias


desarrollador3@bascosta.com

Explicación del proyecto 

myproject/                  # Carpeta raíz del proyecto
│
├── myproject/              # Configuración principal del proyecto
│   ├── __init__.py
│   ├── settings.py         # Configuración del proyecto (BD, apps, middleware, etc.)
│   ├── urls.py             # URLs principales del proyecto
│   ├── wsgi.py             # Configuración para despliegue en servidores WSGI
│   └── asgi.py             # Configuración para despliegue en servidores ASGI
│
├── tasks/                  # Aplicación "tasks" (gestión de tareas)
│   ├── migrations/         # Migraciones de la base de datos
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py            # Registro de modelos en el panel de administración
│   ├── apps.py             # Configuración de la aplicación
│   ├── models.py           # Definición de modelos (Task)
│   ├── views.py            # Lógica de las vistas (CRUD y autenticación)
│   ├── forms.py            # Formularios personalizados (TaskForm)
│   ├── urls.py             # URLs específicas de la aplicación
│   └── templates/          # Plantillas HTML
│       ├── registration/   # Plantillas para registro e inicio de sesión
│       │   ├── register.html
│       │   └── login.html
│       └── tasks/          # Plantillas para el CRUD de tareas
│           ├── task_list.html
│           ├── task_form.html
│           └── task_confirm_delete.html
│
├── manage.py               # Script para gestionar el proyecto (migraciones, servidor, etc.)
└── db.sqlite3              # Base de datos SQLite (se crea automáticamente)



Explicación de cada archivo y carpeta
1. myproject/ (Carpeta raíz del proyecto)
Contiene la configuración principal del proyecto y la aplicación tasks.

settings.py: Aquí se configuran las aplicaciones instaladas, la base de datos, middlewares, plantillas, etc.

Ejemplo: Agregar 'tasks' a INSTALLED_APPS para que Django reconozca la aplicación.

urls.py: Define las rutas principales del proyecto. Aquí se incluyen las URLs de la aplicación tasks.

2. tasks/ (Aplicación de tareas)
Esta aplicación maneja la lógica del CRUD de tareas y la autenticación de usuarios.

models.py: Define los modelos de la base de datos. En este caso, el modelo Task está relacionado con el modelo User de Django.

python
Copy
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
views.py: Contiene la lógica de las vistas (controladores). Aquí se manejan las solicitudes HTTP y se devuelven respuestas.

Ejemplo: Vista para listar tareas:

python
Copy
from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})
forms.py: Define formularios personalizados. En este caso, el formulario para crear y editar tareas.

python
Copy
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'start_time', 'end_time']
urls.py: Define las rutas específicas de la aplicación tasks.

python
Copy
from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/update/<int:pk>/', views.task_update, name='task_update'),
    path('tasks/delete/<int:pk>/', views.task_delete, name='task_delete'),
]
templates/: Contiene las plantillas HTML para renderizar las vistas.

registration/: Plantillas para el registro e inicio de sesión.

tasks/: Plantillas para el CRUD de tareas.

3. manage.py
Es un script que permite ejecutar comandos de Django, como:

python manage.py runserver: Inicia el servidor de desarrollo.

python manage.py makemigrations: Genera migraciones para los modelos.

python manage.py migrate: Aplica las migraciones a la base de datos.

4. db.sqlite3
Es la base de datos SQLite que Django crea automáticamente. Aquí se almacenan los datos de usuarios y tareas.

Flujo del Proyecto
Autenticación:

Un usuario visita la página de registro (/register/) o inicio de sesión (/login/).

Si el registro es exitoso, el usuario es redirigido a la lista de tareas (/tasks/).

CRUD de Tareas:

Un usuario autenticado puede:

Ver la lista de tareas (/tasks/).

Crear una nueva tarea (/tasks/create/).

Editar una tarea existente (/tasks/update/<id>/).

Eliminar una tarea (/tasks/delete/<id>/).

Protección de Vistas:

Las vistas del CRUD están protegidas con el decorador @login_required, lo que asegura que solo los usuarios autenticados puedan acceder a ellas.

Ejemplo de Flujo de una Solicitud
Un usuario visita /tasks/.

Django verifica si el usuario está autenticado (usando @login_required).

Si el usuario no está autenticado, es redirigido a la página de inicio de sesión (/login/).

Si el usuario está autenticado, se ejecuta la vista task_list, que obtiene las tareas del usuario desde la base de datos.

La vista renderiza la plantilla task_list.html con las tareas del usuario.
