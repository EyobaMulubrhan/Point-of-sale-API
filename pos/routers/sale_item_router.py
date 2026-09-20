from uuid import UUID

from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from database import get_db

from schemas.sale_item import (
    SaleItemCreate,
    SaleItemUpdate,
    SaleItemResponse
)

from services.sale_item_service import sale_item_service
from dependencies import require_cashier, require_manager


router = APIRouter(
    prefix="/sale-items",
    tags=["Sale Items"]
)



@router.get("/",response_model=list[SaleItemResponse])
def get_sale_items(db:Session=Depends(get_db),current_user=Depends(require_cashier)):

    return sale_item_service.list_sale_items(db)



@router.get("/{sale_item_id}",response_model=SaleItemResponse)
def get_sale_item(sale_item_id:UUID,db:Session=Depends(get_db),current_user=Depends(require_cashier)):

    return sale_item_service.get_sale_item(db,sale_item_id)



@router.post("/",response_model=SaleItemResponse,status_code=status.HTTP_201_CREATED)
def create_sale_item(data:SaleItemCreate,db:Session=Depends(get_db),current_user=Depends(require_cashier)):

    return sale_item_service.create_sale_item(db,data)



@router.put("/{sale_item_id}",response_model=SaleItemResponse)
def update_sale_item(sale_item_id:UUID,data:SaleItemUpdate,db:Session=Depends(get_db),current_user=Depends(require_manager)):

    return sale_item_service.update_sale_item(db,sale_item_id,data)



@router.delete("/{sale_item_id}")
def delete_sale_item(sale_item_id:UUID,db:Session=Depends(get_db),current_user=Depends(require_manager)):

    return sale_item_service.delete_sale_item(db,sale_item_id)