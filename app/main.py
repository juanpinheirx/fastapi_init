from fastapi import FastAPI

from app.product_model import Product, ProductLibrary, StoragedProduct


app = FastAPI(title="My API")


@app.get("/products", response_model=list[StoragedProduct])
def list_products():
    return ProductLibrary.find_all()


@app.get("/products/{product_id}", response_model=StoragedProduct)
def get_details(product_id: str):
    return ProductLibrary.find_by_id(product_id)


@app.post("/products", status_code=201)
def create_product(product: Product):
    return ProductLibrary.create(product)


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: str):
    try:
        return ProductLibrary.delete(product_id)
    except ValueError:
        return "Product not found", 404


@app.put("/products/{product_id}", status_code=201)
def update_product(product_id: str, product: Product):
    try:
        return ProductLibrary.update(product_id, product)
    except ValueError:
        return "Product not found", 404
