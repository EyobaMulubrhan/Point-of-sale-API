from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class ProductCreate(BaseModel):
    category_id: UUID
    supplier_id: UUID | None = None
    product_name: str
    cost_price: Decimal
    selling_price: Decimal
    quantity: int
    barcode: str | None = None


class ProductUpdate(BaseModel):
    category_id: UUID | None = None
    supplier_id: UUID | None = None
    product_name: str | None = None
    cost_price: Decimal | None = None
    selling_price: Decimal | None = None
    quantity: int | None = None
    barcode: str | None = None


class ProductResponse(BaseModel):
    product_id: UUID
    category_id: UUID
    supplier_id: UUID | None
    product_name: str
    cost_price: Decimal
    selling_price: Decimal
    quantity: int
    barcode: str | None
    created_at: datetime

    class Config:
        from_attributes = True