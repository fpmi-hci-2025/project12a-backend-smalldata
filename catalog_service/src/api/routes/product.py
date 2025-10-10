from uuid import UUID
from fastapi import APIRouter, status, Depends, Query, HTTPException, Security

from api.request.product import ProductCreateModel, ProductUpdateModel
from services.product import ProductService
from exceptions.product import ProductDoesNotExistError
from api.dependencies.product import get_product_service
from api.dependencies.auth import verify_token


router = APIRouter(
    tags=["Products"], prefix="/api/products"
)


@router.get(
    "",
    status_code=status.HTTP_200_OK
)
async def get_products(
    title: str | None = Query(default=None),
    category_id: int | None = Query(default=None),
    price: float | None = Query(default=None),
    description: str | None = Query(default=None),
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.get_products(
        title=title,
        category_id=category_id,
        price=price,
        description=description,
    )


@router.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK
)
async def get_product_by_id(
    product_id: UUID,
    product_service: ProductService = Depends(get_product_service),
):
    try:
        return await product_service.get_product_by_id(product_id=product_id)
    except ProductDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id = {str(product_id)} does not exist"
        )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Security(verify_token)],
)
async def create_product(
    product: ProductCreateModel,
    product_service: ProductService = Depends(get_product_service),
):
    return await product_service.create_product(
        id=product.id,
        title=product.title,
        category_id=product.category_id,
        description=product.description,
        characteristics=product.characteristics,
        created_at=product.created_at,
        amount=product.amount,
        price=product.price,
    )


@router.patch(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    # dependencies=[Security(verify_token)],
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
    # dependencies=[Security(verify_token)],
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
