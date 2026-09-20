from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.user import UserCreate, UserUpdate, UserResponse
from services.user_service import user_service
from dependencies import require_manager


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db), current_user=Depends(require_manager)):
    return user_service.list_users(db)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: UUID, db: Session = Depends(get_db), current_user=Depends(require_manager)):
    return user_service.get_user(db, user_id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db), current_user = Depends(require_manager)):
    return user_service.create_user(db, data)


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: UUID, data: UserUpdate, db: Session = Depends(get_db), current_user=Depends(require_manager)):
    return user_service.update_user(db, user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db), current_user=Depends(require_manager)):
    user_service.delete_user(db, user_id)