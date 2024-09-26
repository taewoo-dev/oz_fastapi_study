from fastapi import APIRouter, Query, UploadFile, status, HTTPException

from products.dto.ProductResponseDto import ProductResponseDto
from products.dto.ProductUpdateRequestDto import ProductUpdateRequestDto
from products.dto.ProductCreateRequestDto import ProductCreateRequestDto

router = APIRouter(prefix="/products", tags=["Products"])


products = [
    {"id": 1, "name": "i-Phone", "price": 1000, "image_name": None},
    {"id": 2, "name": "i-Mac", "price": 2000, "image_name": None},
    {"id": 3, "name": "Galaxy fold", "price": 1000, "image_name": None},
]


@router.get(
    "",
    response_model=list[ProductResponseDto],
    description="제품 전체 조회 API입니다",
    status_code=status.HTTP_200_OK,
)
def get_products_handler(
    max_price: int | None = Query(default=None, ge=100),
    name: str | None = Query(default=None),
):
    return_list = []

    if max_price is None and name is None:
        return [ProductResponseDto.build(product=product) for product in products]

    if max_price and name:
        for product in products:
            if product["price"] <= max_price and product["name"] == name:
                return_list.append(product)

    if max_price and name is None:
        for product in products:
            if product["price"] <= max_price:
                return_list.append(product)

    return [ProductResponseDto(product=product) for product in return_list]


@router.post(
    "",
    response_model=ProductResponseDto,
    description="단일 제품 생성 API입니다",
    status_code=status.HTTP_201_CREATED,
)
def create_product_handler(body: ProductCreateRequestDto):
    product = {
        "id": body.id,
        "name": body.name,
        "price": body.price,
        "image_name": None,
    }
    products.append(product)
    return ProductResponseDto.build(product=product)


@router.get(
    "/{product_id}",
    response_model=ProductResponseDto,
    description="제품 단일 조회 API입니다",
    status_code=status.HTTP_200_OK,
)
def get_product_handler(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return ProductResponseDto.build(product=product)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )


@router.patch(
    "/{product_id}",
    response_model=ProductResponseDto,
    description="단일 제품 업데이트 API입니다",
    status_code=status.HTTP_200_OK,
)
def update_product_handler(product_id: int, body: ProductUpdateRequestDto):
    for product in products:
        if product["id"] == product_id:
            if body.name:
                product["name"] = body.name
            if body.price:
                product["price"] = body.price
            return ProductResponseDto.build(product=product)
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
    response_model=ProductResponseDto,
    description="file upload API입니다",
    status_code=status.HTTP_200_OK,
)
def update_product_file_handler(product_id: int, file: UploadFile):
    for product in products:
        if product["id"] == product_id:
            product["image_name"] = file.filename
            return ProductResponseDto.build(product=product)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found",
    )
