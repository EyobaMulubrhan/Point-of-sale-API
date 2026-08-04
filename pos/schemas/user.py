from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    user_email: EmailStr | None = None
    role: str


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    password: str | None = None
    user_email: EmailStr | None = None
    role: str | None = None


class UserResponse(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    username: str
    user_email: EmailStr | None
    role: str

    class Config:
        from_attributes = True