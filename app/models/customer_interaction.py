from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class CustomerInteraction(Base):
    __tablename__ = "customer_interactions"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    interaction_type = Column(String, nullable=False)

    notes = Column(Text, nullable=True)

    interaction_date = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="interactions")

    user = relationship("User")