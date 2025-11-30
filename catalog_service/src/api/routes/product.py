from uuid import UUID
from fastapi import APIRouter, status, Depends, Query, HTTPException, Security

from api.request.product import ProductCreateModel, ProductUpdateModel
from api.response.product import ProductListResponse, ProductDetailResponse, ProductResponse
from services.product import ProductService
from exceptions.product import ProductDoesNotExistError
from api.dependencies.product import get_product_service
from api.dependencies.auth import verify_token, verify_admin_token


router = APIRouter(
    tags=["Products"], prefix="/api/products"
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ProductListResponse
)
async def get_products(
    title: str | None = Query(default=None, description="Product name filter"),
    category_id: int | None = Query(default=None, description="Category ID filter"),
    product_type: str | None = Query(default=None, description="Product type (телефон, планшет, ноутбук, наушники)"),
    color: str | None = Query(default=None, description="Product color"),
    memory: str | None = Query(default=None, description="Memory/storage size"),
    price_min: float | None = Query(default=None, description="Minimum price"),
    price_max: float | None = Query(default=None, description="Maximum price"),
    brand: str | None = Query(default=None, description="Product brand"),
    description: str | None = Query(default=None, description="Description filter"),
    limit: int = Query(default=50, le=100, description="Limit results"),
    offset: int = Query(default=0, description="Offset for pagination"),
    product_service: ProductService = Depends(get_product_service),
):
    products, total = await product_service.get_products(
        title=title,
        category_id=category_id,
        product_type=product_type,
        color=color,
        memory=memory,
        price_min=price_min,
        price_max=price_max,
        brand=brand,
        description=description,
        limit=limit,
        offset=offset,
    )
    
    return ProductListResponse(
        products=[ProductResponse(**product.__dict__) for product in products],
        total=total,
        limit=limit,
        offset=offset
    )


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductDetailResponse
)
async def get_product_by_id(
    product_id: UUID,
    product_service: ProductService = Depends(get_product_service),
):
    try:
        product = await product_service.get_product_by_id(product_id=product_id)
        return ProductDetailResponse(**product.__dict__)
    except ProductDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id = {str(product_id)} does not exist"
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponse,
    dependencies=[Security(verify_admin_token)],
)
async def create_product(
    product: ProductCreateModel,
    product_service: ProductService = Depends(get_product_service),
):
    created_product = await product_service.create_product(
        id=product.id,
        title=product.title,
        category_id=product.category_id,
        description=product.description,
        characteristics=product.characteristics,
        created_at=product.created_at,
        amount=product.amount,
        price=product.price,
    )
    return ProductResponse(**created_product.__dict__)


@router.patch(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Security(verify_admin_token)],
)
async def update_product(
    product_id: UUID,
    updates: ProductUpdateModel,
    product_service: ProductService = Depends(get_product_service),
):
    try:
        await product_service.update_product(
            product_id=product_id,
            title=updates.title,
            description=updates.description,
            amount=updates.amount,
            price=updates.price,
        )
    except ProductDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id = {str(product_id)} does not exist"
        )
    return {"success": True}


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Security(verify_admin_token)],
)
async def delete_product(
    product_id: UUID,
    product_service: ProductService = Depends(get_product_service),
):
    try:
        await product_service.delete_product(product_id=product_id)
    except ProductDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id = {str(product_id)} does not exist"
        )
    return {"success": True}
