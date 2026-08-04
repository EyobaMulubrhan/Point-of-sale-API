from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.user_repository import user_repository
from schemas.user import UserCreate, UserUpdate


class UserService:

    def get_user(self, db:Session, id:UUID):
        user=user_repository.get(db,id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
        return user


    def list_users(self, db:Session):
        return user_repository.get_all(db)


    def create_user(self, db:Session, data:UserCreate):

        if user_repository.get_by_username(db,data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already exists")

        user_data = data.model_dump()
        password = user_data.pop("password")
        user_data["password_hash"] = password  # stored as-is, no hashing

        return user_repository.create(db,user_data)


    def update_user(self, db:Session, user_id:UUID, data:UserUpdate):

        user=self.get_user(db,user_id)

        update_data = data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password_hash"] = update_data.pop("password")

        return user_repository.update(db,user,update_data)


    def delete_user(self, db:Session, user_id:UUID):

        user=self.get_user(db,user_id)

        user_repository.delete(db,user)

        return {"message":"User deleted successfully"}


user_service=UserService()