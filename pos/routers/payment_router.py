from uuid import UUID

from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from database import get_db
from schemas.payment import PaymentCreate,PaymentUpdate,PaymentResponse
from services.payment_service import payment_service
from dependencies import require_cashier, require_manager


router=APIRouter(prefix="/payments",tags=["Payments"])


@router.get("/",response_model=list[PaymentResponse])
def get_payments(db:Session=Depends(get_db),current_user=Depends(require_cashier)):
    return payment_service.list_payments(db)


@router.get("/{payment_id}",response_model=PaymentResponse)
def get_payment(payment_id:UUID,db:Session=Depends(get_db),current_user=Depends(require_cashier)):
    return payment_service.get_payment(db,payment_id)


@router.post("/",response_model=PaymentResponse,status_code=status.HTTP_201_CREATED)
def create_payment(data:PaymentCreate,db:Session=Depends(get_db),current_user=Depends(require_cashier)):
    return payment_service.create_payment(db,data)


@router.put("/{payment_id}",response_model=PaymentResponse)
def update_payment(payment_id:UUID,data:PaymentUpdate,db:Session=Depends(get_db),current_user=Depends(require_manager)):
    return payment_service.update_payment(db,payment_id,data)


@router.delete("/{payment_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id:UUID,db:Session=Depends(get_db),current_user=Depends(require_manager)):
    payment_service.delete_payment(db,payment_id)