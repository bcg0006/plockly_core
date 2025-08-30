from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserLoginSerializer,
    UserProfileSerializer,
    UserSerializer,
    UserSignupSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    """
    User signup endpoint

    Accepts: email, password, password_confirm
    Returns: user data, JWT tokens, success message
    """
    serializer = UserSignupSerializer(data=request.data)

    if serializer.is_valid():
        try:
            # Create the user
            user = serializer.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Prepare response data
            user_data = UserSerializer(user).data
            tokens = {"access": access_token, "refresh": refresh_token}

            response_data = {
                "user": user_data,
                "tokens": tokens,
                "message": "User registered successfully!",
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # If user creation fails, return error
            return Response(
                {"error": "Failed to create user. Please try again.", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    User login endpoint

    Accepts: email, password
    Returns: user data, JWT tokens, success message
    """
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data["email"].lower().strip()
        password = serializer.validated_data["password"]

        # Try to authenticate with email as username
        user = authenticate(username=email, password=password)

        if user:
            if user.is_active:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                # Prepare response data
                user_data = UserSerializer(user).data
                tokens = {"access": access_token, "refresh": refresh_token}

                response_data = {
                    "user": user_data,
                    "tokens": tokens,
                    "message": "Login successful!",
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Account is disabled. Please contact support."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Invalid credentials. Please check your email and password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    User logout endpoint

    Requires: Authentication
    Returns: Success message
    """
    try:
        # Get the refresh token from request
        refresh_token = request.data.get("refresh_token")

        if refresh_token:
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout successful!"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Refresh token is required for logout."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Exception as e:
        return Response(
            {"error": "Invalid refresh token.", "detail": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    User profile endpoint

    GET: Retrieve user profile
    PUT/PATCH: Update user profile
    Requires: Authentication
    """
    if request.method == "GET":
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method in ["PUT", "PATCH"]:
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=request.method == "PATCH"
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    Refresh JWT token endpoint

    Accepts: refresh token
    Returns: new access token
    """
    try:
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Verify and refresh the token
        refresh = RefreshToken(refresh_token)

        # Check if token is blacklisted
        try:
            refresh.check_blacklist()
        except Exception:
            return Response(
                {"error": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate new access token
        new_access_token = str(refresh.access_token)

        return Response(
            {"access": new_access_token, "message": "Token refreshed successfully!"},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response(
            {"error": "Invalid refresh token.", "detail": str(e)},
            status=status.HTTP_401_UNAUTHORIZED,
        )
