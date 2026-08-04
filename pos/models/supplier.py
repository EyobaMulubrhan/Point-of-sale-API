import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Supplier(Base):

    __tablename__ = "suppliers"

    supplier_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    supplier_name = Column(String, nullable=False)

    supplier_email = Column(String, nullable=False)

    phone_number = Column(String, nullable=True)

    address = Column(String, nullable=True)

    products = relationship("Product", back_populates="supplier")