from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReceiptCreate(BaseModel):

    sale_id: UUID
    receipt_number: str



class ReceiptUpdate(BaseModel):

    receipt_number: str | None = None



class ReceiptResponse(BaseModel):

    receipt_id: UUID
    sale_id: UUID
    issued_date: datetime
    receipt_number: str

    class Config:
        from_attributes=True