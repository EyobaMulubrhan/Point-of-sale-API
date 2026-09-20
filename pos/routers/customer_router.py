from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from services.customer_service import customer_service
from dependencies import require_cashier, require_manager


router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=list[CustomerResponse], status_code=status.HTTP_200_OK)
def get_customers(db: Session = Depends(get_db),current_user=Depends(require_cashier)):
    return customer_service.list_customers(db)


@router.get("/{customer_id}", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
def get_customer(customer_id: UUID, db: Session = Depends(get_db),current_user=Depends(require_cashier)):
    return customer_service.get_customer(db, customer_id)


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db),current_user=Depends(require_cashier)):
    return customer_service.create_customer(db, data)


@router.put("/{customer_id}", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
def update_customer(customer_id: UUID, data: CustomerUpdate, db: Session = Depends(get_db),current_user=Depends(require_cashier)):
    return customer_service.update_customer(db, customer_id, data)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: UUID, db: Session = Depends(get_db),current_user=Depends(require_manager)):
    customer_service.delete_customer(db, customer_id)
    