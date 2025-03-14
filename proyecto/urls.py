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
# Importa las vistas de autenticación
from django.contrib.auth import views as auth_views
# from tasks import views as view_task
from .views import register, user_login

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('', user_login, name='login'),
    path('tasks/', include('tasks.urls')),
]
