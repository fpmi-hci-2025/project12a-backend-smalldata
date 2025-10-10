from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductCreateModel(BaseModel):
    id: UUID
    title: str = Field(..., max_length=255)
    category_id: int
    description: str
    characteristics: dict
    created_at: datetime
    amount: int
    price: float


class ProductUpdateModel(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    amount: Optional[int] = None
    price: Optional[float] = None
