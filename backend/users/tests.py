from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class UserAuthenticationTest(TestCase):
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.signup_url = "/api/auth/signup/"
        self.login_url = "/api/auth/login/"
        self.logout_url = "/api/auth/logout/"
        self.profile_url = "/api/auth/profile/"
        self.refresh_url = "/api/auth/refresh/"

    def test_user_signup_success(self):
        """Test successful user signup with valid email and password"""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }

        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertIn("tokens", response.data)

        # Verify user was created
        user = User.objects.get(email="test@example.com")
        self.assertEqual(user.username, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertTrue(user.is_active)

        # Verify response structure
        user_data = response.data["user"]
        self.assertEqual(user_data["email"], "test@example.com")
        self.assertNotIn("password", user_data)

        # Verify tokens
        tokens = response.data["tokens"]
        self.assertIn("access", tokens)
        self.assertIn("refresh", tokens)

    def test_user_signup_missing_email(self):
        """Test signup fails when email is missing"""
        data = {"password": "testpass123", "password_confirm": "testpass123"}

        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(User.objects.count(), 0)

    def test_user_signup_missing_password(self):
        """Test signup fails when password is missing"""
        data = {"email": "test@example.com", "password_confirm": "testpass123"}

        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertEqual(User.objects.count(), 0)

    def test_user_signup_missing_password_confirm(self):
        """Test signup fails when password confirmation is missing"""
        data = {"email": "test@example.com", "password": "testpass123"}

        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password_confirm", response.data)
        self.assertEqual(User.objects.count(), 0)

    def test_user_signup_passwords_dont_match(self):
        """Test signup fails when passwords don't match"""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "differentpass123",
        }

        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
        self.assertEqual(User.objects.count(), 0)

    def test_user_signup_duplicate_email(self):
        """Test signup fails when email already exists"""
        # Create first user
        User.objects.create_user(
            username="existing@example.com",
            email="existing@example.com",
            password="testpass123",
        )

        # Try to create second user with same email
        data = {
            "email": "existing@example.com",
            "password": "newpass123",
            "password_confirm": "newpass123",
        }

        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_user_signup_invalid_email_format(self):
        """Test signup fails with invalid email format"""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test..test@example.com",
            "test@example..com",
        ]

        for email in invalid_emails:
            with self.subTest(email=email):
                data = {
                    "email": email,
                    "password": "testpass123",
                    "password_confirm": "testpass123",
                }

                response = self.client.post(self.signup_url, data)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn("email", response.data)
                self.assertEqual(User.objects.count(), 0)

    def test_user_signup_weak_password(self):
        """Test signup fails with weak password"""
        weak_passwords = [
            "123",  # Too short
            "password",  # Common word
            "12345678",  # Only numbers
            "abcdefgh",  # Only letters
        ]

        for password in weak_passwords:
            with self.subTest(password=password):
                data = {
                    "email": "test@example.com",
                    "password": password,
                    "password_confirm": password,
                }

                response = self.client.post(self.signup_url, data)

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn("password", response.data)
                self.assertEqual(User.objects.count(), 0)

    def test_user_signup_password_too_short(self):
        """Test signup fails when password is too short"""
        data = {
            "email": "test@example.com",
            "password": "123",
            "password_confirm": "123",
        }

        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertEqual(User.objects.count(), 0)

    def test_user_signup_strong_password_success(self):
        """Test signup succeeds with strong password"""
        strong_passwords = [
            "TestPass123!",
            "MySecureP@ssw0rd",
            "Complex123#Password",
            "Str0ng!P@ss",
        ]

        for password in strong_passwords:
            with self.subTest(password=password):
                data = {
                    "email": f"test{password[:5]}@example.com",
                    "password": password,
                    "password_confirm": password,
                }

                response = self.client.post(self.signup_url, data)

                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertIn("user", response.data)
                self.assertIn("tokens", response.data)

    def test_user_signup_case_insensitive_email(self):
        """Test signup handles email case insensitivity correctly"""
        # Create user with lowercase email
        data1 = {
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }

        response1 = self.client.post(self.signup_url, data1)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Try to create user with same email but different case
        data2 = {
            "email": "TEST@EXAMPLE.COM",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }

        response2 = self.client.post(self.signup_url, data2)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response2.data)

    def test_user_signup_whitespace_handling(self):
        """Test signup handles whitespace in email correctly"""
        # Test with leading/trailing whitespace
        data = {
            "email": "  test@example.com  ",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }

        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify email was stored without whitespace
        user = User.objects.get(email="test@example.com")
        self.assertEqual(user.email, "test@example.com")

    def test_user_signup_response_structure(self):
        """Test signup response has correct structure and data"""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }

        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check response structure
        expected_keys = ["user", "tokens", "message"]
        for key in expected_keys:
            self.assertIn(key, response.data)

        # Check user data structure
        user_data = response.data["user"]
        expected_user_keys = ["id", "username", "email", "is_active", "date_joined"]
        for key in expected_user_keys:
            self.assertIn(key, user_data)

        # Check tokens structure
        tokens = response.data["tokens"]
        expected_token_keys = ["access", "refresh"]
        for key in expected_token_keys:
            self.assertIn(key, tokens)

    def test_user_signup_creates_unique_username(self):
        """Test signup creates unique username from email"""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }

        response = self.client.post(self.signup_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email="test@example.com")
        self.assertEqual(user.username, "test@example.com")

        # Try to create another user with different email
        data2 = {
            "email": "another@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }

        response2 = self.client.post(self.signup_url, data2)

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        user2 = User.objects.get(email="another@example.com")
        self.assertEqual(user2.username, "another@example.com")
        self.assertNotEqual(user.username, user2.username)

    def test_user_login(self):
        """Test user login endpoint."""
        # First create a user
        User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )

        # Test login
        data = {"email": "test@example.com", "password": "testpass123"}

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user", response.data)
        self.assertIn("tokens", response.data)
        self.assertIn("message", response.data)

    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials."""
        # First create a user
        User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )

        # Test login with wrong password
        data = {"email": "test@example.com", "password": "wrongpassword"}

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_user_login_missing_fields(self):
        """Test user login with missing fields."""
        data = {}

        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)

    def test_user_logout(self):
        """Test user logout endpoint."""
        # Create a user and get tokens
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )

        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)

        # Authenticate the client
        self.client.force_authenticate(user=user)

        # Test logout
        data = {"refresh_token": refresh_token}

        response = self.client.post(self.logout_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_user_logout_missing_token(self):
        """Test user logout without refresh token."""
        # Create a user and authenticate
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )

        # Authenticate the client
        self.client.force_authenticate(user=user)

        data = {}

        response = self.client.post(self.logout_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_user_profile_requires_authentication(self):
        """Test that profile endpoint requires authentication."""
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_with_authentication(self):
        """Test profile endpoint with authentication."""
        # Create a user
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )

        # Authenticate the client
        self.client.force_authenticate(user=user)

        # Test profile retrieval
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_token_refresh(self):
        """Test token refresh endpoint."""
        # Create a user and get refresh token
        user = User.objects.create_user(
            username="test@example.com",
            email="test@example.com",
            password="testpass123",
        )

        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)

        # Test token refresh
        data = {"refresh": refresh_token}

        response = self.client.post(self.refresh_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("message", response.data)

    def test_token_refresh_invalid_token(self):
        """Test token refresh with invalid token."""
        data = {"refresh": "invalid_token"}

        response = self.client.post(self.refresh_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
