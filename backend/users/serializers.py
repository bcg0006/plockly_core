from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from rest_framework import serializers


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=254,
        validators=[EmailValidator()],
        help_text="User's email address (will also be used as username)",
    )
    password = serializers.CharField(
        max_length=128, write_only=True, help_text="User's password"
    )
    password_confirm = serializers.CharField(
        max_length=128, write_only=True, help_text="Password confirmation"
    )

    def validate_email(self, value):
        """Validate email format and uniqueness"""
        # Normalize email (lowercase and trim whitespace)
        email = value.lower().strip()

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return email

    def validate_password(self, value):
        """Validate password strength"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return value

    def validate(self, attrs):
        """Validate password confirmation"""
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError(
                {"non_field_errors": ["Passwords do not match."]}
            )

        return attrs

    def create(self, validated_data):
        """Create a new user"""
        email = validated_data["email"]
        password = validated_data["password"]

        # Create user with email as username
        user = User.objects.create_user(
            username=email, email=email, password=password, is_active=True
        )

        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data (read-only, no sensitive information)"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "date_joined"]
        read_only_fields = ["id", "is_active", "date_joined"]


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile updates"""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["id", "is_active", "date_joined"]
