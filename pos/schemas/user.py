from uuid import UUID

from pydantic import BaseModel, EmailStr
from core.roles import Role


class UserCreate(BaseModel):
    full_name: str
    username: str
    password: str
    user_email: EmailStr | None = None
    role: Role

class UserRegister(BaseModel):
    full_name: str
    username: str
    password: str
    user_email: EmailStr | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    username: str | None = None
    password: str | None = None
    user_email: EmailStr | None = None
    role: str | None = None


class UserResponse(BaseModel):
    user_id: UUID
    full_name: str | None = None
    username: str
    user_email: EmailStr | None
    role: str

    class Config:
        from_attributes = True