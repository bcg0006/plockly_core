from django.contrib.auth.models import User
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from .models import Item


class ItemModelTest(TestCase):
    """Test the Item model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_item_creation(self):
        """Test that an item can be created."""
        item = Item.objects.create(
            title="Test Item",
            description="This is a test item",
            owner=self.user,
        )
        self.assertEqual(item.title, "Test Item")
        self.assertEqual(item.description, "This is a test item")
        self.assertEqual(item.owner, self.user)
        self.assertTrue(item.is_active)

    def test_item_string_representation(self):
        """Test the string representation of an item."""
        item = Item.objects.create(
            title="Test Item",
            description="This is a test item",
            owner=self.user,
        )
        self.assertEqual(str(item), "Test Item")

    def test_item_ordering(self):
        """Test that items are ordered by creation date (newest first)."""
        item1 = Item.objects.create(
            title="First Item", description="First", owner=self.user
        )
        item2 = Item.objects.create(
            title="Second Item", description="Second", owner=self.user
        )

        items = Item.objects.all()
        self.assertEqual(items[0], item2)  # Newest first
        self.assertEqual(items[1], item1)  # Oldest last


class ItemAPITest(TestCase):
    """Test the Item API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_item_list_requires_authentication(self):
        """Test that item list requires authentication."""
        # Create unauthenticated client
        client = APIClient()
        response = client.get("/api/items/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_item_list_with_authentication(self):
        """Test that authenticated users can access item list."""
        response = self.client.get("/api/items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_item(self):
        """Test creating a new item."""
        data = {
            "title": "New Test Item",
            "description": "This is a new test item",
        }
        response = self.client.post("/api/items/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify the item was created
        item = Item.objects.get(title="New Test Item")
        self.assertEqual(item.owner, self.user)
        self.assertEqual(item.description, "This is a new test item")

    def test_item_detail(self):
        """Test retrieving item details."""
        item = Item.objects.create(
            title="Test Item",
            description="This is a test item",
            owner=self.user,
        )
        response = self.client.get(f"/api/items/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Item")

    def test_update_item(self):
        """Test updating an item."""
        item = Item.objects.create(
            title="Test Item",
            description="This is a test item",
            owner=self.user,
        )
        data = {"title": "Updated Item", "description": "Updated description"}
        response = self.client.put(f"/api/items/{item.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the item was updated
        item.refresh_from_db()
        self.assertEqual(item.title, "Updated Item")
        self.assertEqual(item.description, "Updated description")

    def test_delete_item(self):
        """Test deleting an item."""
        item = Item.objects.create(
            title="Test Item",
            description="This is a test item",
            owner=self.user,
        )
        response = self.client.delete(f"/api/items/{item.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the item was deleted
        self.assertFalse(Item.objects.filter(id=item.id).exists())
