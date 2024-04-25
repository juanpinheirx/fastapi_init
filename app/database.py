from pymongo import MongoClient
import os

client = MongoClient("mongodb://localhost:27017/")
db = client[os.getenv("DB_NAME", "products_db")]
