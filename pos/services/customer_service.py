from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.customer_repository import customer_repository
from schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:

    def get_customer(self, db: Session, id: UUID):
        customer = customer_repository.get(db, id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return customer

    def list_customers(self, db: Session):
        return customer_repository.get_all(db)

    def create_customer(self, db: Session, data: CustomerCreate):
        return customer_repository.create(db, data.model_dump())

    def update_customer(self, db: Session, customer_id: UUID, data: CustomerUpdate):
        customer = self.get_customer(db, customer_id)
        return customer_repository.update(db, customer, data.model_dump(exclude_unset=True))

    def delete_customer(self, db: Session, customer_id: UUID):
        customer = self.get_customer(db, customer_id)
        if customer.sales:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete a customer that has existing sales",
            )
        customer_repository.delete(db, customer)
        return {"message": "Customer deleted successfully"}


customer_service = CustomerService()