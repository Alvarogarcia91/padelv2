from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    #profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Datos de juego
    ranking = models.IntegerField(default=1000)  # Tipo Elo o ranking inicial
    matches_played = models.IntegerField(default=0)
    matches_won = models.IntegerField(default=0)
    matches_lost = models.IntegerField(default=0)

    # Configuración
    notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class PasswordResetToken(models.Model):
    """Modelo para almacenar tokens de recuperación de contraseña con expiración"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="password_resets")
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        """Revisar si el token ha expirado (ejemplo: 1 hora de validez)"""
        return self.created_at < now() - timedelta(hours=1)

    def __str__(self):
        return f"Reset Token for {self.user.username}"
