"""
URL configuration for padelproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin

from django.urls import path, re_path
from django.urls import include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/users/", include("users.urls")),  # Ruta de usuarios
    path("api-auth/", include("rest_framework.urls")),  # Habilitar autenticación de DRF
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_docs'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_docs'),
]
