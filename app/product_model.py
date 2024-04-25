from dataclasses import dataclass
from app.database import db


@dataclass
class Product:
    name: str
    price: int
    description: str
    image: str


@dataclass
class StoragedProduct(Product):
    _id: str

    def __post_init__(self):
        self._id = str(self._id)


class ProductLibrary:
    _collection = db["products"]

    @classmethod
    def find_all(cls):
        return [StoragedProduct(**product) for product in cls._collection.find()]
