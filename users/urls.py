from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import test_api, register_user  # Importamos la vista de registro

urlpatterns = [
    path("test/", test_api, name="test_api"),  # Endpoint de prueba
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login JWT
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Refresh token
    path("register/", register_user, name="register_user"),  # Registro de usuarios
]
