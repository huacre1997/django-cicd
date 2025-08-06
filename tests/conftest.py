import pytest
from rest_framework.test import APIClient

from apps.products.models import Product


@pytest.fixture
def api_client():
    """
    A Django REST Framework APIClient instance.
    """
    return APIClient()


@pytest.fixture
def product_data():
    """
    Sample data for creating a product.
    """
    return {
        "name": "Test Product",
        "price": "99.99",
        "description": "A fantastic test product.",
    }


@pytest.fixture
def create_product(db):
    """
    Fixture to create a product instance in the database.
    The 'db' fixture ensures database access.
    """

    def _create_product(**kwargs):
        defaults = {
            "name": "Default Product",
            "price": "10.00",
            "description": "A default product for testing.",
        }
        defaults.update(kwargs)
        return Product.objects.create(**defaults)

    return _create_product
