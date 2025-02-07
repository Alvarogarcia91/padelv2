from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        """Verifica que el email no esté registrado"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        """Crea un usuario con estado activo o inactivo según la configuración"""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        
        # Verificar si la validación por email está activada
        if settings.EMAIL_VERIFICATION_REQUIRED:
            user.is_active = False  # Usuario inactivo hasta que confirme el email
        user.save()
        
        return user
