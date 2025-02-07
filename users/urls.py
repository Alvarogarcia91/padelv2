from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import test_api  # Mantiene la prueba de API

urlpatterns = [
    path("test/", test_api, name="test_api"),  # Endpoint de prueba
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login JWT
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Refresh token
]
