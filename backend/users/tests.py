import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class UserAuthenticationTest(TestCase):
    """Test user authentication endpoints."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
        }

    def test_user_registration(self):
        """Test user registration endpoint."""
        response = self.client.post("/api/auth/register/", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify response contains expected data
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertIn("user", response.data)
        
        # Verify user was created in database
        user = User.objects.get(username="testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))

    def test_user_registration_missing_fields(self):
        """Test user registration with missing fields."""
        incomplete_data = {"username": "testuser"}
        response = self.client.post("/api/auth/register/", incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_user_registration_duplicate_username(self):
        """Test user registration with duplicate username."""
        # Create first user
        User.objects.create_user(
            username="testuser",
            email="first@example.com",
            password="testpass123",
        )
        
        # Try to create second user with same username
        response = self.client.post("/api/auth/register/", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_user_login(self):
        """Test user login endpoint."""
        # Create user first
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        
        # Test login
        login_data = {
            "username": "testuser",
            "password": "testpass123",
        }
        response = self.client.post("/api/auth/login/", login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify response contains expected data
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)
        self.assertIn("user", response.data)

    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials."""
        # Create user first
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        
        # Test login with wrong password
        login_data = {
            "username": "testuser",
            "password": "wrongpassword",
        }
        response = self.client.post("/api/auth/login/", login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_user_login_missing_fields(self):
        """Test user login with missing fields."""
        response = self.client.post("/api/auth/login/", {"username": "testuser"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_user_profile_requires_authentication(self):
        """Test that profile endpoint requires authentication."""
        response = self.client.get("/api/auth/profile/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_with_authentication(self):
        """Test profile endpoint with authentication."""
        # Create and authenticate user
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.client.force_authenticate(user=user)
        
        response = self.client.get("/api/auth/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "test@example.com")

    def test_token_refresh(self):
        """Test token refresh endpoint."""
        # Create user and get refresh token
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        
        # Test token refresh
        response = self.client.post(
            "/api/auth/refresh/", {"refresh_token": refresh_token}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify response contains new tokens
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_token_refresh_invalid_token(self):
        """Test token refresh with invalid token."""
        response = self.client.post(
            "/api/auth/refresh/", {"refresh_token": "invalid_token"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_user_logout(self):
        """Test user logout endpoint."""
        # Create user and get refresh token
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        
        # Authenticate the user
        self.client.force_authenticate(user=user)
        
        # Test logout
        response = self.client.post(
            "/api/auth/logout/", {"refresh_token": refresh_token}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_user_logout_missing_token(self):
        """Test user logout without refresh token."""
        # Create and authenticate user
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.client.force_authenticate(user=user)
        
        response = self.client.post("/api/auth/logout/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
