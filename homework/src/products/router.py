from fastapi import APIRouter, Path, Query

router = APIRouter(prefix="/products", tags=["Products"])


products = [
    {"id": 1, "name": "i-Phone", "price": 1000},
    {"id": 2, "name": "i-Mac", "price": 2000},
    {"id": 3, "name": "Galaxy fold", "price": 1000},
]


@router.get("")
def get_products_handler(
    max_price: int | None = Query(default=None, ge=100),
    name: str | None = Query(default=None),
):
    return_list = []

    if max_price is None and name is None:
        return products

    if max_price and name:
        for product in products:
            if product["price"] <= max_price and product["name"] == name:
                return_list.append(product)

    if max_price and name is None:
        for product in products:
            if product["price"] <= max_price:
                return_list.append(product)

    return return_list
