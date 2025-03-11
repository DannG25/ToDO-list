# ToDo-List
Este proyecto es un gestor de tareas desarrollado con Django, que permite a los usuarios crear, editar, eliminar y visualizar tareas de manera sencilla. Está diseñado para ser intuitivo y fácil de usar, con una interfaz amigable y responsiva.

**Características Principales**
**Autenticación de Usuarios:**

* Registro e inicio de sesión.

* Recuperación de contraseña.

**Gestión de Tareas:**

* Crear, editar, eliminar y visualizar tareas.

* Asignar prioridades (alta, media, baja).

* Establecer fechas de vencimiento.

Interfaz Amigable:

* Diseño responsivo basado en SB Admin 2.

* Formularios estilizados con Bootstrap.

Seguridad:

* Protección de rutas con @login_required.

* Uso de CSRF tokens en formularios.()

# Tecnologías Utilizadas

**Backend:**

* Django (Python)

* Django Authentication System

**Frontend:**

* HTML5, CSS3

* Bootstrap 4

* SB Admin 2 (Plantilla de administración)

**Base de Datos:**

* SQLite (por defecto en desarrollo)

* Compatible con PostgreSQL, MySQL, etc.

# Otras Herramientas:

* Django Widget Tweaks (para estilizar formularios)

* FontAwesome (para íconos)

# Instalación y Configuración
Sigue estos pasos para configurar el proyecto en tu entorno local:

#  Requisitos Previos
* Python 3.8 o superior.
* Pip (gestor de paquetes de Python).
  
# Capturas de Pantalla
* Página de Inicio de Sesión
  
* Login

* Lista de Tareas
  
* Task List

Formulario de Creación de Tareas

# Pasos para Instalar
* Clona el repositorio:
* git clone https://github.com/tu-usuario/tu-repositorio.git
* cd tu-repositorio
  
**Crea un entorno virtual:**

* python -m venv venv
* source venv/bin/activate  # En Windows: venv\Scripts\activate
  
**Instala las dependencias:**

* pip install -r requirements.txt
  
**Realiza las migraciones:**

* python manage.py migrate
  
**Crea un superusuario (opcional):**

* python manage.py createsuperuser
  
**Ejecuta el servidor de desarrollo:**

* python manage.py runserver

 **Accede al proyecto en tu navegador:**
 
_http://127.0.0.1:8000/_

# Estructura del Proyecto

gestor-tareas/

├── manage.py

├── tasks/

│   ├── migrations/

│   ├── templates/

│   │   ├── registration/

│   │   │   ├── login.html

│   │   │   ├── register.html

│   │   ├── tasks/

│   │   │   ├── task_list.html

│   │   │   ├── task_form.html

│   │   │   ├── task_delete.html

│   ├── models.py

│   ├── views.py

│   ├── forms.py

│   ├── urls.py

├── static/

│   ├── css/

│   ├── js/

│   ├── vendor/

├── requirements.txt

├── README.md

# Contacto
Si tienes alguna pregunta o sugerencia, no dudes en contactarme:

Email: [danielga252009@hotmail.com]

GitHub: [https://github.com/DannG25]

