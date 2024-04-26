import pytest
from app.product_model import ProductLibrary


def test_get_products_is_empty(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


def test_get_products(client):
    data = {
        "name": "notebook",
        "price": 100,
        "description": "notebook",
        "image": "notebook.jpg",
    }
    ProductLibrary._collection.insert_one(data)
    response = client.get("/products")
    assert response.status_code == 200
    for item in response.json():
        assert "name" in item
        assert "price" in item
        assert "description" in item
        assert "image" in item
        assert "_id" in item


def test_get_details(client):
    product_id = ProductLibrary.find_all()[0].id
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == {
        "name": "notebook",
        "price": 100,
        "description": "notebook",
        "image": "notebook.jpg",
        "_id": str(product_id),
    }


def test_post_products(client):
    data = {
        "name": "notebook2",
        "price": 1002,
        "description": "notebook2",
        "image": "notebook2.jpg",
    }
    response = client.post("/products", json=data)
    assert response.status_code == 201
    assert response.json() == "Product created successfully"
    assert ProductLibrary.find_all()[-1].name == "notebook2"


def test_delete_product(client):
    product_id = ProductLibrary.find_all()[0].id
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 204
    with pytest.raises(ValueError):
        ProductLibrary.find_by_id(product_id)


def test_update_product(client):
    product_id = ProductLibrary.find_all()[0].id
    data = {
        "name": "notebook2",
        "price": 1002,
        "description": "notebook2",
        "image": "notebook2.jpg",
    }
    response = client.put(f"/products/{product_id}", json=data)
    assert response.status_code == 201
    assert ProductLibrary.find_by_id(product_id).price == 1002
