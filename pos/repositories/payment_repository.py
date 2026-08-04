from uuid import UUID

from sqlalchemy.orm import Session

from models.payment import Payment


class PaymentRepository:

    def __init__(self):
        self.model=Payment


    def get(self,db:Session,id:UUID):
        return db.get(self.model,id)


    def get_all(self,db:Session):
        return db.query(self.model).all()


    def create(self,db:Session,data:dict):

        payment=self.model(**data)

        db.add(payment)
        db.commit()
        db.refresh(payment)

        return payment


    def update(self,db:Session,db_obj:Payment,data:dict):

        for field,value in data.items():
            setattr(db_obj,field,value)

        db.commit()
        db.refresh(db_obj)

        return db_obj


    def delete(self,db:Session,db_obj:Payment):

        db.delete(db_obj)
        db.commit()

        return True


payment_repository=PaymentRepository()