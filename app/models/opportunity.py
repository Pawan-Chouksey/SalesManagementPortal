from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Date
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship

from app.database import Base


class Opportunity(Base):

    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer,ForeignKey("customers.id"),nullable=False)

    owner_id = Column(Integer,ForeignKey("users.id"),nullable=False)

    title = Column(String, nullable=False)

    deal_value = Column(Float, nullable=False)

    stage = Column(String, default="Lead")

    probability = Column(Integer, default=10)

    expected_close_date = Column(Date, nullable=True)

    competitor_name = Column(String, nullable=True)

    loss_reason = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="opportunities")

    owner = relationship("User", back_populates="opportunities")
