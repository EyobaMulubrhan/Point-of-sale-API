from uuid import UUID

from pydantic import BaseModel, EmailStr


class SupplierCreate(BaseModel):
    supplier_name: str
    supplier_email: EmailStr
    phone_number: str | None = None
    address: str | None = None


class SupplierUpdate(BaseModel):
    supplier_name: str | None = None
    supplier_email: EmailStr | None = None
    phone_number: str | None = None
    address: str | None = None


class SupplierResponse(BaseModel):
    supplier_id: UUID
    supplier_name: str
    supplier_email: EmailStr
    phone_number: str | None
    address: str | None

    class Config:
        from_attributes = True