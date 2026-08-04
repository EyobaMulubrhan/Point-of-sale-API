import uuid

from sqlalchemy import Column,DateTime,ForeignKey,String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Receipt(Base):

    __tablename__="receipts"


    receipt_id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,index=True)

    sale_id=Column(UUID(as_uuid=True),ForeignKey("sales.sale_id"),nullable=False)

    issued_date=Column(DateTime(timezone=True),server_default=func.now())

    receipt_number=Column(String,unique=True,nullable=False)


    sale=relationship("Sale",back_populates="receipt")