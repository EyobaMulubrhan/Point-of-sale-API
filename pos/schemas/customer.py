from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr | None = None
    phone_number: str | None = None


class CustomerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None


class CustomerResponse(BaseModel):
    customer_id: UUID
    first_name: str
    last_name: str
    email: EmailStr | None
    phone_number: str | None
    created_at: datetime

    class Config:
        from_attributes = True