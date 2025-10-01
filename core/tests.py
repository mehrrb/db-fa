from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Category, ProductInstance, ProductType, Recipe


class CategoryModelTest(TestCase):
    """Test cases for Category model."""

    def test_category_creation(self):
        """Test category creation."""
        category = Category.objects.create(name="Test Category")
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(str(category), "Test Category")

    def test_category_str(self):
        """Test category string representation."""
        category = Category(name="Test Category")
        self.assertEqual(str(category), "Test Category")


class ProductTypeModelTest(TestCase):
    """Test cases for ProductType model."""

    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(name="Test Category")
        self.product_type = ProductType.objects.create(
            name="Test Product",
            base_weight=100,
            waste=10,
            unit="gram",
            category=self.category,
        )

    def test_product_type_creation(self):
        """Test product type creation."""
        self.assertEqual(self.product_type.name, "Test Product")
        self.assertEqual(self.product_type.base_weight, 100)
        self.assertEqual(self.product_type.waste, 10)
        self.assertEqual(self.product_type.unit, "gram")
        self.assertEqual(self.product_type.category, self.category)

    def test_waste_ratio_calculation(self):
        """Test waste ratio calculation."""
        self.product_type.base_weight = 100
        self.product_type.waste = 10
        self.assertEqual(self.product_type.waste_ratio, 0.1)

    def test_waste_ratio_zero_base_weight(self):
        """Test waste ratio when base weight is zero."""
        product_type = ProductType(base_weight=0, waste=10)
        self.assertEqual(product_type.waste_ratio, 0)

    def test_product_type_str(self):
        """Test product type string representation."""
        self.assertEqual(str(self.product_type), "Test Product")


class ProductInstanceModelTest(TestCase):
    """Test cases for ProductInstance model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(name="Test Category")
        self.product_type = ProductType.objects.create(
            name="Test Product",
            base_weight=100,
            waste=10,
            unit="gram",
            category=self.category,
        )
        self.product_instance = ProductInstance.objects.create(
            product_type=self.product_type,
            total_weight=1000,
            price_per_kilo=10000,
            unit="gram",
            user=self.user,
        )

    def test_product_instance_creation(self):
        """Test product instance creation."""
        self.assertEqual(self.product_instance.product_type, self.product_type)
        self.assertEqual(self.product_instance.total_weight, 1000)
        self.assertEqual(self.product_instance.price_per_kilo, 10000)
        self.assertEqual(self.product_instance.user, self.user)

    def test_automatic_calculations_on_save(self):
        """Test automatic calculations when saving."""
        # Check that calculations are performed
        self.assertIsNotNone(self.product_instance.waste_weight)
        self.assertIsNotNone(self.product_instance.net_weight)
        self.assertIsNotNone(self.product_instance.total_price)

        # Verify calculations are correct
        expected_waste = 1000 * self.product_type.waste_ratio
        expected_net = 1000 - expected_waste
        expected_price = (10000 * 1000) / 1000 + (10000 * expected_waste) / 1000

        self.assertAlmostEqual(
            self.product_instance.waste_weight, expected_waste, places=2
        )
        self.assertAlmostEqual(self.product_instance.net_weight, expected_net, places=2)
        self.assertAlmostEqual(
            self.product_instance.total_price, expected_price, places=2
        )

    def test_product_instance_str(self):
        """Test product instance string representation."""
        str_repr = str(self.product_instance)
        self.assertIn(self.product_instance.product_type.name, str_repr)
        self.assertIn(str(self.product_instance.total_weight), str_repr)


class RecipeModelTest(TestCase):
    """Test cases for Recipe model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            description="Test Description",
            user=self.user,
            selling_price=50000,
        )

    def test_recipe_creation(self):
        """Test recipe creation."""
        self.assertEqual(self.recipe.name, "Test Recipe")
        self.assertEqual(self.recipe.user, self.user)
        self.assertEqual(self.recipe.total_cost, 0)  # Default value

    def test_recipe_str(self):
        """Test recipe string representation."""
        self.assertEqual(str(self.recipe), "Test Recipe")

    def test_calculate_total_cost_empty_recipe(self):
        """Test total cost calculation for empty recipe."""
        total_cost = self.recipe.calculate_total_cost()
        self.assertEqual(total_cost, 0)

    def test_calculate_profit(self):
        """Test profit calculation."""
        self.recipe.selling_price = 50000
        self.recipe.total_cost = 30000
        profit = self.recipe.calculate_profit()
        self.assertEqual(profit, 20000)

    def test_calculate_profit_no_selling_price(self):
        """Test profit calculation when no selling price."""
        self.recipe.selling_price = None
        profit = self.recipe.calculate_profit()
        self.assertEqual(profit, 0)

    def test_calculate_profit_percentage(self):
        """Test profit percentage calculation."""
        self.recipe.selling_price = 50000
        self.recipe.total_cost = 30000
        percentage = self.recipe.calculate_profit_percentage()
        expected = (50000 - 30000) / 30000 * 100
        self.assertAlmostEqual(percentage, expected, places=2)

    def test_calculate_profit_percentage_zero_cost(self):
        """Test profit percentage when cost is zero."""
        self.recipe.selling_price = 50000
        self.recipe.total_cost = 0
        percentage = self.recipe.calculate_profit_percentage()
        self.assertEqual(percentage, 0)


class BusinessLogicTest(TestCase):
    """Test business logic calculations."""

    def test_waste_calculation(self):
        """Test waste calculation logic."""
        waste_percentage = 10
        total_weight = 1000

        waste_ratio = waste_percentage / 100
        waste_weight = total_weight * waste_ratio
        net_weight = total_weight - waste_weight

        self.assertEqual(waste_ratio, 0.1)
        self.assertEqual(waste_weight, 100)
        self.assertEqual(net_weight, 900)

    def test_price_calculation(self):
        """Test price calculation logic."""
        price_per_kilo = 10000
        total_weight = 1000
        waste_weight = 100

        # Base price
        base_price = (price_per_kilo * total_weight) / 1000
        self.assertEqual(base_price, 10000)

        # Waste cost
        waste_cost = (price_per_kilo * waste_weight) / 1000
        self.assertEqual(waste_cost, 1000)

        # Total price
        total_price = base_price + waste_cost
        self.assertEqual(total_price, 11000)

    def test_profit_calculation(self):
        """Test profit calculation logic."""
        selling_price = 50000
        total_cost = 30000

        profit = selling_price - total_cost
        profit_percentage = (profit / total_cost) * 100

        self.assertEqual(profit, 20000)
        self.assertAlmostEqual(profit_percentage, 66.67, places=2)

    def test_decimal_precision(self):
        """Test decimal precision for financial calculations."""
        price = Decimal("100.50")
        quantity = Decimal("2.5")
        total = price * quantity
        self.assertEqual(total, Decimal("251.25"))

    def test_edge_cases(self):
        """Test edge cases."""
        # Zero values
        base_weight = 0
        waste = 10
        waste_ratio = waste / base_weight if base_weight > 0 else 0
        self.assertEqual(waste_ratio, 0)

        # Large numbers
        large_weight = 1000000
        large_price = 1000000
        result = large_weight * large_price
        self.assertGreater(result, 0)

        # Small numbers
        small_weight = 0.001
        small_price = 0.01
        result = small_weight * small_price
        self.assertGreater(result, 0)
