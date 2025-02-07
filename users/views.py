from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@api_view(["GET"])
@permission_classes([AllowAny])  # Permitir acceso sin autenticación
def test_api(request):
    return Response({"message": "Django REST Framework is working!"})

@swagger_auto_schema(
    method="post",
    request_body=RegisterSerializer,
    responses={201: "User created successfully with tokens", 400: "Bad Request"}
)
@api_view(["POST"])
@permission_classes([AllowAny])  # Permitir registro sin autenticación previa
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Generar tokens JWT para el nuevo usuario
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({
            "message": "User created successfully",
            "access": access,
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
