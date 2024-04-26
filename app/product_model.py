from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import ReturnDocument
from app.database import db


class Product(BaseModel):
    name: str
    price: int
    description: str
    image: str


class StoragedProduct(Product):
    id: str = Field(alias="_id")


class ProductLibrary:
    _collection = db["products"]

    @classmethod
    def find_all(cls):
        return [
            StoragedProduct(_id=str(product.pop("_id")), **product)
            for product in cls._collection.find()
        ]

    @classmethod
    def find_by_id(cls, product_id):
        found_prod = cls._collection.find_one({"_id": ObjectId(product_id)})
        if found_prod:
            return StoragedProduct(_id=str(found_prod.pop("_id")), **found_prod)
        else:
            raise ValueError("Product not found")

    @classmethod
    def create(cls, product: Product):
        cls._collection.insert_one(vars(product))
        return "Product created successfully"

    @classmethod
    def delete(cls, product_id):
        removed = cls._collection.delete_one({"_id": ObjectId(product_id)})
        if removed.deleted_count == 0:
            raise ValueError("Product not found")

    @classmethod
    def update(cls, product_id, product: Product):
        updated = cls._collection.find_one_and_update(
            {"_id": ObjectId(product_id)},
            {"$set": vars(product)},
            return_document=ReturnDocument.AFTER,
        )
        if updated is None:
            raise ValueError("Product not found")
        return StoragedProduct(_id=str(updated.pop("_id")), **updated)
