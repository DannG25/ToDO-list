from rest_framework import serializers
from apps.tasks.models import Task, EmailConfig


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Task.
    Incluye todos los campos del modelo.
    """
    class Meta:
        model = Task
        fields = '__all__'


class EmailConfigSerializer(serializers.ModelSerializer):
    """
    Serializer para la configuración del servidor de correo electrónico con MailHog.
    """
    class Meta:
        model = EmailConfig
        fields = '__all__'
        extra_kwargs = {
            # Oculta la contraseña en respuestas
            'email_host_password': {'write_only': True},
        }

    def validate_email_port(self, value):
        """
        Valida que el puerto esté dentro de un rango válido (0-65535).
        """
        if not (0 <= value <= 65535):
            raise serializers.ValidationError(
                "El puerto debe estar entre 0 y 65535."
            )
        return value

    def set_mailhog_defaults(self, validated_data, instance=None):
        """
        Establece valores predeterminados de MailHog si no se proporcionan.
        Si es una actualización, solo establece valores predeterminados si aún no existen en la instancia.
        """
        defaults = {
            "email_host": "localhost",
            "email_port": 1025,
            "email_use_tls": False,
            "email_use_ssl": False,
            "email_host_user": "",
            "email_host_password": "",
        }
        for key, value in defaults.items():
            if instance:
                # Si el valor en la instancia ya existe, no lo sobrescribimos
                validated_data.setdefault(key, getattr(instance, key, value))
            else:
                # En creación, asignamos siempre el valor predeterminado si no lo envían
                validated_data.setdefault(key, value)

        return validated_data

    def create(self, validated_data):
        """
        Crea una configuración de correo con valores predeterminados para MailHog si no se proporcionan.
        """
        validated_data = self.set_mailhog_defaults(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza la configuración de correo manteniendo valores predeterminados de MailHog si no se proporcionan.
        """
        validated_data = self.set_mailhog_defaults(validated_data)
        return super().update(instance, validated_data)
