from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class PaymentCreate(BaseModel):
    sale_id: UUID
    customer_id: UUID | None = None
    paid_amount: Decimal


class PaymentUpdate(BaseModel):
    customer_id: UUID | None = None
    paid_amount: Decimal | None = None


class PaymentResponse(BaseModel):
    payment_id: UUID
    sale_id: UUID
    customer_id: UUID | None
    payment_date: datetime
    paid_amount: Decimal

    class Config:
        from_attributes=True