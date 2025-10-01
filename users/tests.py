from django.contrib.auth.models import User
from django.test import TestCase

from .models import Profile


class UserModelTest(TestCase):
    """Test cases for User model."""

    def test_user_creation(self):
        """Test user creation."""
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))

    def test_user_str(self):
        """Test user string representation."""
        user = User.objects.create_user(username="testuser")
        self.assertEqual(str(user), "testuser")


class ProfileModelTest(TestCase):
    """Test cases for Profile model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_profile_creation(self):
        """Test profile creation."""
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(str(profile), f"{self.user.username} Profile")

    def test_profile_one_to_one_relationship(self):
        """Test one-to-one relationship with User."""
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(self.user.profile, profile)

    def test_profile_str(self):
        """Test profile string representation."""
        profile = Profile.objects.create(user=self.user)
        expected = f"{self.user.username} Profile"
        self.assertEqual(str(profile), expected)


class AuthenticationTest(TestCase):
    """Test authentication functionality."""

    def test_user_login(self):
        """Test user login."""
        user = User.objects.create_user(username="testuser", password="testpass123")

        # Test password check
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.check_password("wrongpassword"))

    def test_user_password_change(self):
        """Test user password change."""
        user = User.objects.create_user(username="testuser", password="oldpassword")

        # Change password
        user.set_password("newpassword")
        user.save()

        # Test new password
        self.assertTrue(user.check_password("newpassword"))
        self.assertFalse(user.check_password("oldpassword"))

    def test_user_attributes(self):
        """Test user attributes."""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="testpass123",
        )

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)


class DataValidationTest(TestCase):
    """Test data validation logic."""

    def test_positive_values(self):
        """Test that values are positive."""
        values = [100, 50.5, 0.1, 1000]
        for value in values:
            self.assertGreater(value, 0)

    def test_string_operations(self):
        """Test string operations."""
        text = "Hello World"
        self.assertEqual(len(text), 11)
        self.assertEqual(text.upper(), "HELLO WORLD")
        self.assertEqual(text.lower(), "hello world")

    def test_list_operations(self):
        """Test list operations."""
        numbers = [1, 2, 3, 4, 5]
        self.assertEqual(len(numbers), 5)
        self.assertEqual(sum(numbers), 15)
        self.assertEqual(max(numbers), 5)
        self.assertEqual(min(numbers), 1)

    def test_dict_operations(self):
        """Test dictionary operations."""
        data = {"name": "Test", "age": 25, "city": "Tehran"}
        self.assertIn("name", data)
        self.assertEqual(data["age"], 25)
        self.assertEqual(len(data), 3)
