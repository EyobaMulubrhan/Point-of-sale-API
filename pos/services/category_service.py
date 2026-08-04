from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.category_repository import category_repository
from schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:

    def get_category(self, db: Session, id: UUID):
        category = category_repository.get(db, id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return category

    def list_categories(self, db: Session):
        return category_repository.get_all(db)

    def create_category(self, db: Session, data: CategoryCreate):
        return category_repository.create(db, data.model_dump())

    def update_category(self, db: Session, category_id: UUID, data: CategoryUpdate):
        category = self.get_category(db, category_id)
        return category_repository.update(db, category, data.model_dump(exclude_unset=True))

    def delete_category(self, db: Session, category_id: UUID):
        category = self.get_category(db, category_id)
        if category.products:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete a category that still has products assigned to it",
            )
        category_repository.delete(db, category)
        return {"message": "Category deleted successfully"}


category_service = CategoryService()