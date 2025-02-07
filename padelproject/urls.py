from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración de Swagger con soporte para JWT
schema_view = get_schema_view(
    openapi.Info(
        title="Padel API",
        default_version='v1',
        description="Documentación de la API de la app de pádel",
        terms_of_service="https://www.tusitio.com/terms/",
        contact=openapi.Contact(email="soporte@tusitio.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],  # Evita que Swagger use Basic Auth por defecto
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/users/", include("users.urls")),  # Rutas de autenticación y usuarios
    path("api-auth/", include("rest_framework.urls")),  # Habilitar autenticación de DRF

    # Documentación de Swagger con soporte para JWT
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_docs'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_docs'),
]
