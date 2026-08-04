from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.supplier_repository import supplier_repository
from schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:

    def get_supplier(self, db: Session, id: UUID):
        supplier = supplier_repository.get(db, id)
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
        return supplier

    def list_suppliers(self, db: Session):
        return supplier_repository.get_all(db)

    def create_supplier(self, db: Session, data: SupplierCreate):
        return supplier_repository.create(db, data.model_dump())

    def update_supplier(self, db: Session, supplier_id: UUID, data: SupplierUpdate):
        supplier = self.get_supplier(db, supplier_id)
        return supplier_repository.update(db, supplier, data.model_dump(exclude_unset=True))

    def delete_supplier(self, db: Session, supplier_id: UUID):
        supplier = self.get_supplier(db, supplier_id)
        if supplier.products:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete a supplier that still has products assigned to it",
            )
        supplier_repository.delete(db, supplier)
        return {"message": "Supplier deleted successfully"}


supplier_service = SupplierService()