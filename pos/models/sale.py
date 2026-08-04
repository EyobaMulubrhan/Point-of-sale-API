import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Sale(Base):

    __tablename__ = "sales"

    sale_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.customer_id"), nullable=True)

    sale_amount = Column(Numeric(10,2), nullable=False)

    sale_date = Column(DateTime(timezone=True), server_default=func.now())

    tax = Column(Numeric(10,2), nullable=False)

    discount = Column(Numeric(10,2), nullable=False)


    user = relationship("User", back_populates="sales")

    customer = relationship("Customer", back_populates="sales")

    items = relationship("SaleItem", back_populates="sale")

    payment = relationship("Payment", back_populates="sale")

    receipt = relationship("Receipt", back_populates="sale")