from pydantic import BaseModel


class ProductUpdateRequestDto(BaseModel):
    name: str
    price: int
