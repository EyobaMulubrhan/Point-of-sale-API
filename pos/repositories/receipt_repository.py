from uuid import UUID

from sqlalchemy.orm import Session

from models.receipt import Receipt


class ReceiptRepository:

    def __init__(self):
        self.model=Receipt


    def get(self,db:Session,id:UUID):
        return db.get(self.model,id)


    def get_all(self,db:Session):
        return db.query(self.model).all()


    def create(self,db:Session,data:dict):

        receipt=self.model(**data)

        db.add(receipt)
        db.commit()
        db.refresh(receipt)

        return receipt


    def update(self,db:Session,db_obj:Receipt,data:dict):

        for field,value in data.items():
            setattr(db_obj,field,value)

        db.commit()
        db.refresh(db_obj)

        return db_obj


    def delete(self,db:Session,db_obj:Receipt):

        db.delete(db_obj)
        db.commit()

        return True



receipt_repository=ReceiptRepository()