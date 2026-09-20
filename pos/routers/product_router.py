from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from services.product_service import product_service
from dependencies import require_manager,require_cashier


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def get_products(db: Session = Depends(get_db),current_user=Depends(require_cashier)):
    return product_service.list_products(db)


@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product(product_id: UUID, db: Session = Depends(get_db),current_user=Depends(require_cashier)):
    return product_service.get_product(db, product_id)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(get_db),current_user=Depends(require_manager)):
    return product_service.create_product(db, data)


@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def update_product(product_id: UUID, data: ProductUpdate, db: Session = Depends(get_db),current_user=Depends(require_manager)):
    return product_service.update_product(db, product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: UUID, db: Session = Depends(get_db),current_user=Depends(require_manager)):
    product_service.delete_product(db, product_id)

    