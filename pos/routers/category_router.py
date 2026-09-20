from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from services.category_service import category_service
from dependencies import require_manager,require_cashier



router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
def get_categories(db: Session = Depends(get_db),current_user=Depends(require_cashier)):
    return category_service.list_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def get_category(category_id: UUID, db: Session = Depends(get_db),current_user=Depends(require_manager)):
    return category_service.get_category(db, category_id)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db),current_user=Depends(require_manager)):
    return category_service.create_category(db, data)


@router.put("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def update_category(category_id: UUID, data: CategoryUpdate, db: Session = Depends(get_db),current_user=Depends(require_manager)):
    return category_service.update_category(db, category_id, data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: UUID, db: Session = Depends(get_db),current_user=Depends(require_manager)):
    category_service.delete_category(db, category_id)