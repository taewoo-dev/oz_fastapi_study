from fastapi import APIRouter, Query, UploadFile, status, HTTPException

from products.dto import (
    ProductResponse,
    ProductCreateRequest,
    ProductUpdateRequest,
)

router = APIRouter(prefix="/products", tags=["Products"])


products = [
    {"id": 1, "name": "i-Phone", "price": 1000, "image_name": None},
    {"id": 2, "name": "i-Mac", "price": 2000, "image_name": None},
    {"id": 3, "name": "Galaxy fold", "price": 1000, "image_name": None},
]


@router.get(
    "",
    response_model=list[ProductResponse],
    description="제품 전체 조회 API입니다",
    status_code=status.HTTP_200_OK,
)
def get_products_handler(
    max_price: int | None = Query(default=None, ge=100),
    name: str | None = Query(default=None),
):
    return_list = []

    if max_price is None and name is None:
        return [ProductResponse.build(product=product) for product in products]

    if max_price and name:
        for product in products:
            if product["price"] <= max_price and product["name"] == name:
                return_list.append(product)

    if max_price and name is None:
        for product in products:
            if product["price"] <= max_price:
                return_list.append(product)

    return [ProductResponse(product=product) for product in return_list]


@router.post(
    "",
    response_model=ProductResponse,
    description="단일 제품 생성 API입니다",
    status_code=status.HTTP_201_CREATED,
)
def create_product_handler(body: ProductCreateRequest):
    product = {
        "id": body.id,
        "name": body.name,
        "price": body.price,
        "image_name": None,
    }
    products.append(product)
    return ProductResponse.build(product=product)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    description="제품 단일 조회 API입니다",
    status_code=status.HTTP_200_OK,
)
def get_product_handler(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return ProductResponse.build(product=product)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
    description="단일 제품 업데이트 API입니다",
    status_code=status.HTTP_200_OK,
)
def update_product_handler(product_id: int, body: ProductUpdateRequest):
    for product in products:
        if product["id"] == product_id:
            if body.name:
                product["name"] = body.name
            if body.price:
                product["price"] = body.price
            return ProductResponse.build(product=product)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )


@router.delete(
    "/{product_id}",
    description="단일 제품 삭제 API입니다",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product_handler(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )


@router.patch(
    "/file/{product_id}",
    response_model=ProductResponse,
    description="file upload API입니다",
    status_code=status.HTTP_200_OK,
)
def update_product_file_handler(product_id: int, file: UploadFile):
    for product in products:
        if product["id"] == product_id:
            product["image_name"] = file.filename
            return ProductResponse.build(product=product)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )
