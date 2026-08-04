from uuid import UUID

from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from database import get_db

from schemas.receipt import ReceiptCreate,ReceiptUpdate,ReceiptResponse
from services.receipt_service import receipt_service


router=APIRouter(prefix="/receipts",tags=["Receipts"])


@router.get("/",response_model=list[ReceiptResponse])
def get_receipts(db:Session=Depends(get_db)):
    return receipt_service.list_receipts(db)


@router.get("/{receipt_id}",response_model=ReceiptResponse)
def get_receipt(receipt_id:UUID,db:Session=Depends(get_db)):
    return receipt_service.get_receipt(db,receipt_id)


@router.post("/",response_model=ReceiptResponse,status_code=status.HTTP_201_CREATED)
def create_receipt(data:ReceiptCreate,db:Session=Depends(get_db)):
    return receipt_service.create_receipt(db,data)


@router.put("/{receipt_id}",response_model=ReceiptResponse)
def update_receipt(receipt_id:UUID,data:ReceiptUpdate,db:Session=Depends(get_db)):
    return receipt_service.update_receipt(db,receipt_id,data)


@router.delete("/{receipt_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_receipt(receipt_id:UUID,db:Session=Depends(get_db)):
    receipt_service.delete_receipt(db,receipt_id)