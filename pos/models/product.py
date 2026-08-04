import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base


class Product(Base):

    __tablename__ = "products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.category_id"), nullable=False)

    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.supplier_id"), nullable=True)

    product_name = Column(String, nullable=False)

    cost_price = Column(Numeric(10, 2), nullable=False)

    selling_price = Column(Numeric(10, 2), nullable=False)

    quantity = Column(Integer, nullable=False)

    barcode = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="products")

    supplier = relationship("Supplier", back_populates="products")

    sale_items=relationship("SaleItem",back_populates="product")