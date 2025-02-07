from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register_user, activate_user, request_password_reset, reset_password

urlpatterns = [
    path("register/", register_user, name="register_user"),  # Registro con email verification
    path("activate/<str:token>/", activate_user, name="activate_user"),  # Activación de cuenta
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login JWT
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Refresh token
    path("password-reset/", request_password_reset, name="password_reset_request"),  # Solicitar restablecimiento
    path("password-reset/<str:token>/", reset_password, name="password_reset_confirm"),  # Confirmar cambio de contraseña
]
