from app.main import app
from fastapi.testclient import TestClient
import pytest

from app.product_model import ProductLibrary


@pytest.fixture(autouse=True)
def client():
    return TestClient(app)


@pytest.fixture(autouse=True, scope="session")
def clear_database():
    ProductLibrary._collection.delete_many({})
    yield
    ProductLibrary._collection.delete_many({})
