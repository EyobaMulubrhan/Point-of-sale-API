from uuid import UUID

from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from repositories.payment_repository import payment_repository
from repositories.sale_repository import sale_repository
from schemas.payment import PaymentCreate, PaymentUpdate


class PaymentService:


    def get_payment(self,db:Session,id:UUID):

        payment=payment_repository.get(db,id)

        if not payment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Payment not found")

        return payment



    def list_payments(self,db:Session):
        return payment_repository.get_all(db)



    def create_payment(self,db:Session,data:PaymentCreate):

        sale=sale_repository.get(db,data.sale_id)

        if not sale:
            raise HTTPException(status_code=404,detail="Sale not found")

        return payment_repository.create(db,data.model_dump())



    def update_payment(self,db:Session,payment_id:UUID,data:PaymentUpdate):

        payment=self.get_payment(db,payment_id)

        return payment_repository.update(db,payment,data.model_dump(exclude_unset=True))



    def delete_payment(self,db:Session,payment_id:UUID):

        payment=self.get_payment(db,payment_id)

        payment_repository.delete(db,payment)

        return {"message":"Payment deleted successfully"}


payment_service=PaymentService()