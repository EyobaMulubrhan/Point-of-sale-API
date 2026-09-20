import uuid

from sqlalchemy import Column, String ,Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):

    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    full_name = Column(String, nullable=False)

    username = Column(String, unique=True, nullable=False)

    password_hash = Column(String, nullable=False)

    user_email = Column(String, nullable=True)

    role = Column(String, nullable=False)

    is_active=Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sales = relationship("Sale", back_populates="user")