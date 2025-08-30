from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                }
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

    return Response(
        {"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if username and email and password:
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "user": {"id": user.id, "username": user.username, "email": user.email},
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        {"error": "Username, email and password required"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
def logout(request):
    try:
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response(
                {"message": "Successfully logged out"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST
            )
    except Exception:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    Custom token refresh endpoint that handles token rotation and blacklisting.
    This ensures old refresh tokens are invalidated after use.
    """
    try:
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                {"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Create new tokens with rotation
        refresh = RefreshToken(refresh_token)

        # Blacklist the old refresh token
        refresh.blacklist()

        # Generate new tokens
        new_refresh = (
            RefreshToken.for_user(request.user)
            if hasattr(request, "user") and request.user.is_authenticated
            else RefreshToken()
        )

        return Response(
            {
                "access_token": str(new_refresh.access_token),
                "refresh_token": str(new_refresh),
            },
            status=status.HTTP_200_OK,
        )

    except Exception:
        return Response(
            {"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(["GET"])
def profile(request):
    return Response(
        {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
        }
    )
