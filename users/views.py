from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([AllowAny])  # Permitir acceso sin autenticación
def test_api(request):
    return Response({"message": "Django REST Framework is working!"})
