from uuid import UUID

from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from repositories.receipt_repository import receipt_repository
from repositories.sale_repository import sale_repository
from schemas.receipt import ReceiptCreate, ReceiptUpdate


class ReceiptService:


    def get_receipt(self,db:Session,id:UUID):

        receipt=receipt_repository.get(db,id)

        if not receipt:
            raise HTTPException(status_code=404,detail="Receipt not found")

        return receipt



    def list_receipts(self,db:Session):

        return receipt_repository.get_all(db)



    def create_receipt(self,db:Session,data:ReceiptCreate):

        sale=sale_repository.get(db,data.sale_id)

        if not sale:
            raise HTTPException(status_code=404,detail="Sale not found")


        return receipt_repository.create(db,data.model_dump())



    def update_receipt(self,db:Session,receipt_id:UUID,data:ReceiptUpdate):

        receipt=self.get_receipt(db,receipt_id)

        return receipt_repository.update(db,receipt,data.model_dump(exclude_unset=True))



    def delete_receipt(self,db:Session,receipt_id:UUID):

        receipt=self.get_receipt(db,receipt_id)

        receipt_repository.delete(db,receipt)

        return {"message":"Receipt deleted successfully"}


receipt_service=ReceiptService()