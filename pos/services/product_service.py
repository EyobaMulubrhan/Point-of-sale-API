from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.product_repository import product_repository
from repositories.category_repository import category_repository
from repositories.supplier_repository import supplier_repository
from schemas.product import ProductCreate, ProductUpdate


class ProductService:

    def get_product(self, db: Session, id: UUID):
        product = product_repository.get(db, id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return product

    def list_products(self, db: Session):
        return product_repository.get_all(db)

    def create_product(self, db: Session, data: ProductCreate):
        if not category_repository.get(db, data.category_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        if data.supplier_id and not supplier_repository.get(db, data.supplier_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

        return product_repository.create(db, data.model_dump())

    def update_product(self, db: Session, product_id: UUID, data: ProductUpdate):
        product = self.get_product(db, product_id)

        update_data = data.model_dump(exclude_unset=True)

        if "category_id" in update_data and not category_repository.get(db, update_data["category_id"]):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        if update_data.get("supplier_id") and not supplier_repository.get(db, update_data["supplier_id"]):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

        return product_repository.update(db, product, update_data)

    def delete_product(self, db: Session, product_id: UUID):
        product = self.get_product(db, product_id)
        if product.sale_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete a product that appears in existing sales",
            )
        product_repository.delete(db, product)
        return {"message": "Product deleted successfully"}


product_service = ProductService()