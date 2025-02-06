from django.db import models
from django.contrib.auth.models import User

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
