from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class SaleCreate(BaseModel):

    customer_id: UUID | None = None
    tax: Decimal
    discount: Decimal



class SaleUpdate(BaseModel):

    tax: Decimal | None = None
    discount: Decimal | None = None



class SaleResponse(BaseModel):

    sale_id: UUID
    user_id: UUID
    customer_id: UUID | None
    sale_amount: Decimal
    sale_date: datetime
    tax: Decimal
    discount: Decimal


    class Config:
        from_attributes = True