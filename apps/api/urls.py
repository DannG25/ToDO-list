"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.views.generic import RedirectView
# from .views import TaskListCreateView, TaskRetrieveUpdateDestroyView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from apps.api.viewset import HelloWorldViewSet, TaskViewSet, HelloWorldAPIView, EmailConfigViewSet


router = DefaultRouter()
router.register(r'hello-world', HelloWorldViewSet, basename='hello-world')
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'email-config', EmailConfigViewSet, basename='email-config')

urlpatterns = [
    # Rutas del router
    path('api-v1.0/', include(router.urls)),

    # endPoints Autorización JWT
    path('api-v1.0/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api-v1.0/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    # Tasks EndPoints
    path('api-v1.0/hello-world2/', HelloWorldAPIView.as_view(), name='hello-world2'),
]
