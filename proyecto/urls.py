"""
 Configuración de URL para el proyecto.

La lista `urlpatterns` enruta URLs a vistas. Para más información consulte:
 https://docs.djangoproject.com/en/4.2/topics/http/urls/
Ejemplos:
Función views
 1. Añade una importación: from my_app import views
 2. Añade una URL a urlpatterns: path('') views.home.
 Añadir una URL a urlpatterns: path('', views.home, name='home')Vistas basadas en clases
 1. Añadir una importación: from other_app.views import Home
 2. Añadir una URL a urlpatterns: path('', views.home, name='home')
 Añade una URL a urlpatterns: path('', Home.as_view(), name='home')Incluyendo otra URLconf
 1. Importa la función include(): from django.urls import include, path
 2. Añade una URL a urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),

    # URLs de autenticación
    path('register/', views.register, name='register'),  # Registro de usuarios
    path('login/', views.user_login, name='login'),     # Inicio de sesión
    path('logout/', auth_views.LogoutView.as_view(),
         name='logout'),  # Cerrar sesión

    # URLs para recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # Redirigir la raíz a la página de login
    path('', RedirectView.as_view(url='login/')),

    # Incluir las URLs de la aplicación tasks
    path('tasks/', include('tasks.urls')),
]
