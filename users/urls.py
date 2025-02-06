from django.urls import path
from .views import test_api  # Asegúrate de que tienes esta vista en `views.py`

urlpatterns = [
    path("test/", test_api, name="test_api"),
]
