#!/usr/bin/env python3
"""
Test script for the signup API endpoint
Run this after starting the Django server with: python manage.py runserver
"""

import requests

# API endpoint
SIGNUP_URL = "http://localhost:8000/api/auth/signup/"


def test_signup_success():
    """Test successful user signup"""
    print("🧪 Testing successful signup...")

    data = {
        "email": "test@example.com",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
    }

    response = requests.post(SIGNUP_URL, json=data)

    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        print("✅ Signup successful!")
        result = response.json()
        print(f"User ID: {result['user']['id']}")
        print(f"Email: {result['user']['email']}")
        print(f"Access Token: {result['tokens']['access'][:50]}...")
        print(f"Message: {result['message']}")
    else:
        print("❌ Signup failed!")
        print(f"Error: {response.text}")

    print("-" * 50)


def test_signup_duplicate_email():
    """Test signup with duplicate email"""
    print("🧪 Testing duplicate email signup...")

    data = {
        "email": "test@example.com",  # Same email as above
        "password": "AnotherPass123!",
        "password_confirm": "AnotherPass123!",
    }

    response = requests.post(SIGNUP_URL, json=data)

    print(f"Status Code: {response.status_code}")
    if response.status_code == 400:
        print("✅ Correctly rejected duplicate email!")
        result = response.json()
        print(f"Error: {result.get('email', 'Unknown error')}")
    else:
        print("❌ Should have rejected duplicate email!")
        print(f"Response: {response.text}")

    print("-" * 50)


def test_signup_password_mismatch():
    """Test signup with password mismatch"""
    print("🧪 Testing password mismatch...")

    data = {
        "email": "newuser@example.com",
        "password": "TestPass123!",
        "password_confirm": "DifferentPass123!",
    }

    response = requests.post(SIGNUP_URL, json=data)

    print(f"Status Code: {response.status_code}")
    if response.status_code == 400:
        print("✅ Correctly rejected password mismatch!")
        result = response.json()
        print(f"Error: {result.get('non_field_errors', 'Unknown error')}")
    else:
        print("❌ Should have rejected password mismatch!")
        print(f"Response: {response.text}")

    print("-" * 50)


def test_signup_weak_password():
    """Test signup with weak password"""
    print("🧪 Testing weak password...")

    data = {
        "email": "weakuser@example.com",
        "password": "123",
        "password_confirm": "123",
    }

    response = requests.post(SIGNUP_URL, json=data)

    print(f"Status Code: {response.status_code}")
    if response.status_code == 400:
        print("✅ Correctly rejected weak password!")
        result = response.json()
        print(f"Error: {result.get('password', 'Unknown error')}")
    else:
        print("❌ Should have rejected weak password!")
        print(f"Response: {response.text}")

    print("-" * 50)


def test_signup_invalid_email():
    """Test signup with invalid email format"""
    print("🧪 Testing invalid email format...")

    data = {
        "email": "invalid-email",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!",
    }

    response = requests.post(SIGNUP_URL, json=data)

    print(f"Status Code: {response.status_code}")
    if response.status_code == 400:
        print("✅ Correctly rejected invalid email!")
        result = response.json()
        print(f"Error: {result.get('email', 'Unknown error')}")
    else:
        print("❌ Should have rejected invalid email!")
        print(f"Response: {response.text}")

    print("-" * 50)


if __name__ == "__main__":
    print("🚀 Testing Plockly v2 Signup API")
    print("=" * 50)

    try:
        # Test various scenarios
        test_signup_success()
        test_signup_duplicate_email()
        test_signup_password_mismatch()
        test_signup_weak_password()
        test_signup_invalid_email()

        print("🎉 All tests completed!")

    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure Django server is running:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"❌ Error: {e}")
