from uuid import UUID

from sqlalchemy.orm import Session

from models.sale_item import SaleItem


class SaleItemRepository:

    def __init__(self):
        self.model=SaleItem


    def get(self,db:Session,id:UUID):
        return db.get(self.model,id)


    def get_all(self,db:Session):
        return db.query(self.model).all()


    def create(self,db:Session,data:dict):

        sale_item=self.model(**data)

        db.add(sale_item)
        db.commit()
        db.refresh(sale_item)

        return sale_item


    def update(self,db:Session,db_obj:SaleItem,data:dict):

        for field,value in data.items():
            setattr(db_obj,field,value)

        db.commit()
        db.refresh(db_obj)

        return db_obj


    def delete(self,db:Session,db_obj:SaleItem):

        db.delete(db_obj)
        db.commit()

        return True


sale_item_repository=SaleItemRepository()