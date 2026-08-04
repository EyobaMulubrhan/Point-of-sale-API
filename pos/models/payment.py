import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Payment(Base):

    __tablename__="payments"

    payment_id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    sale_id=Column(UUID(as_uuid=True), ForeignKey("sales.sale_id"), nullable=False)

    customer_id=Column(UUID(as_uuid=True), ForeignKey("customers.customer_id"), nullable=True)

    payment_date=Column(DateTime(timezone=True), server_default=func.now())

    paid_amount=Column(Numeric(10,2), nullable=False)

    sale=relationship("Sale", back_populates="payment")