from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import status

from database import get_db
from services.auth_service import authenticate, register
from schemas.user import UserCreate,UserResponse


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    return register(db, data)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return authenticate(
        db,
        form_data.username,
        form_data.password,
    )