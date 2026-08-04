from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.sale_repository import sale_repository
from schemas.sale import SaleCreate, SaleUpdate


class SaleService:


    def get_sale(self, db: Session, id: UUID):

        sale = sale_repository.get(db,id)

        if not sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sale not found"
            )

        return sale



    def list_sales(self, db: Session):

        return sale_repository.get_all(db)



    def create_sale(self, db: Session, data: SaleCreate):

        sale_data = data.model_dump()

        sale_data["sale_amount"] = 0

        return sale_repository.create(db,sale_data)



    def update_sale(self, db: Session, sale_id: UUID, data: SaleUpdate):

        sale = self.get_sale(db,sale_id)

        return sale_repository.update(
            db,
            sale,
            data.model_dump(exclude_unset=True)
        )



    def delete_sale(self, db: Session, sale_id: UUID):

        sale = self.get_sale(db,sale_id)

        if sale.items or sale.payment or sale.receipt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete a sale that has items, a payment, or a receipt attached to it",
            )

        sale_repository.delete(db,sale)

        return {
            "message":"Sale deleted successfully"
        }



sale_service = SaleService()