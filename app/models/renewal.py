from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database import Base


class Renewal(Base):
    __tablename__ = "renewals"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"),nullable=False)

    contract_start = Column(Date, nullable=True)

    contract_end = Column(Date, nullable=True)

    renewal_status = Column(String, default="pending")

    reminder_date = Column(Date, nullable=True)

    customer = relationship("Customer", back_populates="renewals")