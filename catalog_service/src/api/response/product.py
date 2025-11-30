from datetime import datetime
from uuid import UUID
from typing import List, Dict, Any

from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: UUID
    title: str
    category_id: int
    description: str
    characteristics: Dict[str, Any]
    created_at: datetime
    amount: int
    price: float

    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    limit: int
    offset: int


class ProductDetailResponse(ProductResponse):
    pass