from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.sale_item_repository import sale_item_repository
from repositories.product_repository import product_repository
from repositories.sale_repository import sale_repository
from schemas.sale_item import SaleItemCreate, SaleItemUpdate


class SaleItemService:

    def get_sale_item(self, db:Session, id:UUID):
        sale_item=sale_item_repository.get(db,id)
        if not sale_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Sale item not found")

        return sale_item


    def list_sale_items(self, db:Session):
        return sale_item_repository.get_all(db)


    def create_sale_item(self, db:Session, data:SaleItemCreate):
        sale=sale_repository.get(db,data.sale_id)

        if not sale:
            raise HTTPException(status_code=404,detail="Sale not found")
        
        product=product_repository.get(db,data.product_id)

        if not product:
            raise HTTPException(status_code=404,detail="Product not found")

        if product.quantity < data.quantity:
            raise HTTPException(status_code=400,detail="Not enough product stock")

        item_data=data.model_dump()
        subtotal=data.quantity * data.product_price
        item_data["subtotal"]=subtotal
        product.quantity-=data.quantity
        sale.sale_amount+=subtotal
        sale_item=sale_item_repository.create(db,item_data)

        db.commit()
        db.refresh(sale)
        return sale_item


    def update_sale_item(self, db:Session, sale_item_id:UUID, data:SaleItemUpdate):
        item=self.get_sale_item(db,sale_item_id)
        update_data=data.model_dump(exclude_unset=True)
        new_quantity=update_data.get("quantity",item.quantity)
        new_price=update_data.get("product_price",item.product_price)

        if "quantity" in update_data:
            product=product_repository.get(db,item.product_id)
            quantity_delta=new_quantity-item.quantity

            if quantity_delta>0 and product.quantity<quantity_delta:
                raise HTTPException(status_code=400,detail="Not enough product stock")

            product.quantity-=quantity_delta

        old_subtotal=item.subtotal
        new_subtotal=new_quantity*new_price
        update_data["subtotal"]=new_subtotal
        sale=sale_repository.get(db,item.sale_id)
        sale.sale_amount+=(new_subtotal-old_subtotal)
        updated_item=sale_item_repository.update(db,item,update_data)

        db.commit()
        db.refresh(sale)

        return updated_item


    def delete_sale_item(self, db:Session, sale_item_id:UUID):
        item=self.get_sale_item(db,sale_item_id)
        product=product_repository.get(db,item.product_id)
        sale=sale_repository.get(db,item.sale_id)

        if product:
            product.quantity+=item.quantity
        if sale:
            sale.sale_amount-=item.subtotal

        sale_item_repository.delete(db,item)
        return {"message":"Sale item deleted successfully"}


sale_item_service=SaleItemService()