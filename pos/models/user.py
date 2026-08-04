import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class User(Base):

    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    first_name = Column(String, nullable=False)

    last_name = Column(String, nullable=False)

    username = Column(String, unique=True, nullable=False)

    password_hash = Column(String, nullable=False)

    user_email = Column(String, nullable=True)

    role = Column(String, nullable=False)

    sales = relationship("Sale", back_populates="user")