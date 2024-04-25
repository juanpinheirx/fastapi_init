from fastapi import FastAPI

from app.product_model import ProductLibrary, StoragedProduct


app = FastAPI(title="My API")


@app.get("/products", response_model=list[StoragedProduct])
def list_products():
    return ProductLibrary.find_all()
