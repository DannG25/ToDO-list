from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from apps.tasks.models import *
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar y crear tareas.
    """
    queryset = Task.objects.all()  # pylint: disable=no-member
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)  # pylint: disable=no-member

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para recuperar, actualizar y eliminar una tarea específica.
    """
    queryset = Task.objects.all()  # pylint: disable=no-member
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)  # pylint: disable=no-member


class TaskResolveView(APIView):
    """
    Vista para marcar una tarea como resuelta.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # Obtiene la tarea o devuelve un 404 si no existe
        task = get_object_or_404(Task, pk=pk, user=request.user)

        # Verifica si la tarea ya está resuelta
        if task.resuelto:
            return Response(
                {'status': 'La tarea ya está resuelta'},
                status=status.HTTP_200_OK
            )

        # Marca la tarea como resuelta
        task.resuelto = True
        task.save()

        # Retorna una respuesta exitosa
        return Response(
            {'status': 'Tarea marcada como resuelta'},
            status=status.HTTP_200_OK
        )
