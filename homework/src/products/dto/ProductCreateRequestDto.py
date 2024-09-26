from pydantic import BaseModel


class ProductCreateRequestDto(BaseModel):
    id: int
    name: str
    price: int
