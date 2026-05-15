from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class CustomerContact(Base):
    __tablename__ = "customer_contacts"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    name = Column(String, nullable=False)

    email = Column(String, nullable=True)

    phone = Column(String, nullable=True)

    designation = Column(String, nullable=True)

    customer = relationship("Customer", back_populates="contacts")
