from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.sale import SaleCreate, SaleUpdate, SaleResponse
from services.sale_service import sale_service
from dependencies import require_cashier, require_manager



router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)



@router.get("/", response_model=list[SaleResponse])
def get_sales(db: Session = Depends(get_db),current_user=Depends(require_cashier)):

    return sale_service.list_sales(db)



@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: UUID, db: Session = Depends(get_db),current_user=Depends(require_cashier)):

    return sale_service.get_sale(db,sale_id)



@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(data: SaleCreate, db: Session = Depends(get_db),current_user=Depends(require_cashier)):

    return sale_service.create_sale(db,data,current_user)



@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(sale_id: UUID,data: SaleUpdate,db: Session = Depends(get_db),current_user=Depends(require_manager)):

    return sale_service.update_sale(db,sale_id,data)



@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(sale_id: UUID,db: Session = Depends(get_db),current_user=Depends(require_manager)):

    sale_service.delete_sale(db,sale_id)