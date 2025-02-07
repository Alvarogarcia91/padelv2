from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from .models import PasswordResetToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import uuid


@swagger_auto_schema(
    method="post",
    request_body=RegisterSerializer,
    responses={
        201: openapi.Response(
            description="User created successfully",
            examples={
                "application/json": {
                    "message": "User created successfully",
                    "access": "ACCESS_TOKEN_GENERADO",
                    "refresh": "REFRESH_TOKEN_GENERADO"
                }
            },
        ),
        400: openapi.Response(
            description="Bad Request - Missing fields",
            examples={
                "application/json": {
                    "username": ["This field is required."],
                    "password": ["This field is required."]
                }
            },
        ),
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    """Registro de usuario con verificación de email opcional"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        if settings.EMAIL_VERIFICATION_REQUIRED:
            activation_token = str(uuid.uuid4())
            user.first_name = activation_token
            user.is_active = False
            user.save()

            activation_link = f"http://127.0.0.1:8000/api/users/activate/{activation_token}/"
            send_mail(
                "Activate your account",
                f"Click the link to activate your account: {activation_link}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response({"message": "User created successfully. Check your email for activation."}, status=status.HTTP_201_CREATED)

        else:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User created successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def activate_user(request, token):
    """Activa la cuenta si el token es válido y genera el JWT"""
    user = get_object_or_404(User, first_name=token)

    # Activar usuario y limpiar el token de activación
    user.is_active = True
    user.first_name = ""
    user.save()

    # Generar access y refresh tokens tras la activación
    refresh = RefreshToken.for_user(user)
    
    return Response({
        "message": "Account activated successfully",
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, format="email"),
        },
    ),
    responses={
        200: openapi.Response(
            description="Si el email existe, se envía un enlace de recuperación.",
            examples={
                "application/json": {
                    "message": "If the email exists, a reset link has been sent."
                }
            },
        ),
        400: openapi.Response(
            description="Error en la solicitud",
            examples={
                "application/json": {
                    "error": "Email is required"
                }
            },
        ),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def request_password_reset(request):
    """Solicitar un restablecimiento de contraseña enviando un email con el enlace"""
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.filter(email=email).first()
    if not user:
        return Response({"message": "If the email exists, a reset link has been sent."}, status=status.HTTP_200_OK)

    # Generar un token único y guardarlo en la base de datos
    reset_token = get_random_string(length=64)
    PasswordResetToken.objects.create(user=user, token=reset_token)

    # Enviar email con el enlace de restablecimiento
    reset_link = f"http://127.0.0.1:8000/api/users/password-reset/{reset_token}/"
    send_mail(
        "Reset Your Password",
        f"Click the link to reset your password: {reset_link}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    return Response({"message": "If the email exists, a reset link has been sent."}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["password"],
        properties={
            "password": openapi.Schema(type=openapi.TYPE_STRING, format="password"),
        },
    ),
    responses={
        200: openapi.Response(
            description="Contraseña restablecida correctamente.",
            examples={
                "application/json": {
                    "message": "Password reset successfully"
                }
            },
        ),
        400: openapi.Response(
            description="Error en la solicitud",
            examples={
                "application/json": {
                    "error": "Invalid or expired token"
                }
            },
        ),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request, token):
    """Restablecer la contraseña si el token es válido"""
    new_password = request.data.get("password")
    if not new_password:
        return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

    reset_token = PasswordResetToken.objects.filter(token=token).first()
    if not reset_token or reset_token.is_expired():
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

    user = reset_token.user
    user.set_password(new_password)
    user.save()

    # Eliminar el token después de su uso
    reset_token.delete()

    return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
