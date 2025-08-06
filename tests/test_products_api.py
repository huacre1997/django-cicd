import pytest
from django.urls import reverse
from rest_framework import status

from apps.products.models import Product

pytestmark = pytest.mark.django_db


def test_list_products(api_client, create_product):
    """
    Test listing all products.
    """
    product1 = create_product(name="Laptop", price="1200.00")
    product2 = create_product(name="Mouse", price="25.00")

    url = reverse("product-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Laptop"
    assert response.data[1]["name"] == "Mouse"


def test_create_product(api_client, product_data):
    """
    Test creating a new product.
    """
    url = reverse("product-list")
    response = api_client.post(url, product_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.count() == 1
    assert Product.objects.get().name == product_data["name"]
    assert float(Product.objects.get().price) == float(product_data["price"])


def test_create_product_invalid_data(api_client):
    """
    Test creating a product with invalid data (e.g., missing name).
    """
    url = reverse("product-list")
    invalid_data = {"price": "10.00"}
    response = api_client.post(url, invalid_data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
    assert Product.objects.count() == 0


def test_retrieve_product(api_client, create_product):
    """
    Test retrieving a single product by ID.
    """
    product = create_product(name="Keyboard", price="75.00")
    url = reverse("product-detail", kwargs={"pk": product.pk})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Keyboard"
    assert float(response.data["price"]) == 75.00


def test_update_product(api_client, create_product):
    """
    Test updating an existing product.
    """
    product = create_product(name="Old Name", price="50.00")
    url = reverse("product-detail", kwargs={"pk": product.pk})
    updated_data = {"name": "New Name", "price": "60.00"}
    response = api_client.put(url, updated_data, format="json")

    assert response.status_code == status.HTTP_200_OK
    product.refresh_from_db()
    assert product.name == "New Name"
    assert float(product.price) == 60.00


def test_partial_update_product(api_client, create_product):
    """
    Test partially updating an existing product.
    """
    product = create_product(
        name="Original Name", price="100.00", description="Original Desc"
    )
    url = reverse("product-detail", kwargs={"pk": product.pk})
    partial_data = {"description": "Updated Description"}
    response = api_client.patch(url, partial_data, format="json")

    assert response.status_code == status.HTTP_200_OK
    product.refresh_from_db()
    assert product.name == "Original Name"
    assert product.description == "Updated Description"


def test_delete_product(api_client, create_product):
    """
    Test deleting a product.
    """
    product = create_product(name="To Be Deleted", price="1.00")
    url = reverse("product-detail", kwargs={"pk": product.pk})
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Product.objects.count() == 0
    assert not Product.objects.filter(pk=product.pk).exists()
