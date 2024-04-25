from app.main import app
from fastapi.testclient import TestClient
import pytest
from app.product_model import ProductLibrary


@pytest.fixture(autouse=True)
def clear_database():
    ProductLibrary._collection.delete_many({})
    yield
    ProductLibrary._collection.delete_many({})


def test_get_products_is_empty():
    client = TestClient(app)
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


def test_get_products():
    data = {
        "name": "notebook",
        "price": 100,
        "description": "notebook",
        "image": "notebook.jpg",
    }
    ProductLibrary._collection.insert_one(data)
    client = TestClient(app)
    response = client.get("/products")
    assert response.status_code == 200
    for item in response.json():
        assert "name" in item
        assert "price" in item
        assert "description" in item
        assert "image" in item
        assert "_id" in item
