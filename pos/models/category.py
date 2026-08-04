import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Category(Base):

    __tablename__="categories"

    category_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,index=True)

    category_name=Column(String,nullable=False)

    description=Column(String,nullable=True)

    products=relationship("Product",back_populates="category")