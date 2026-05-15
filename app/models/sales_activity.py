from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship

from app.database import Base


class SalesActivity(Base):

    __tablename__ = "sales_activities"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    activity_type = Column(String, nullable=False)

    title = Column(String, nullable=False)

    notes = Column(Text, nullable=True)

    activity_date = Column(DateTime, default=datetime.utcnow )

    follow_up_date = Column(DateTime, nullable=True )

    status = Column(String, default="pending")

    user = relationship("User")

    customer = relationship("Customer", back_populates="sales_activities")