from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    id: int
    name: str
    price: int


class UpdateProductRequest(BaseModel):
    name: str | None = None
    price: int | None = None


class ProductResponse(BaseModel):
    name: str
    price: int


class ProductsListResponse(BaseModel):
    products: list[ProductResponse]


class CreateProductResponse(BaseModel):
    message: str


class UpdateProductResponse(BaseModel):
    message: str
