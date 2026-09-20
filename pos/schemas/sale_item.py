from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class SaleItemCreate(BaseModel):

    sale_id: UUID
    product_id: UUID
    quantity: int


class SaleItemUpdate(BaseModel):

    quantity: int | None = None


class SaleItemResponse(BaseModel):

    sale_item_id: UUID
    sale_id: UUID
    product_id: UUID
    quantity: int
    product_price: Decimal
    subtotal: Decimal


    class Config:
        from_attributes = True