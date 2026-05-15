from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base


class AccountPlan(Base):
    __tablename__ = "account_plans"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    goals = Column(Text, nullable=True)

    renewal_value = Column(Integer, nullable=True)

    customer = relationship("Customer", back_populates="account_plans")