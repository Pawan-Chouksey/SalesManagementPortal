from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String, nullable=False)

    address = Column(String, nullable=True)

    website = Column(String, nullable=True)

    assigned_rep_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    
    assigned_rep = relationship("User", back_populates="customers")

    contacts = relationship("CustomerContact",back_populates="customer",cascade="all, delete-orphan")

    interactions = relationship("CustomerInteraction",back_populates="customer",cascade="all, delete-orphan")

    account_plans = relationship("AccountPlan", back_populates="customer", cascade="all, delete-orphan")

    renewals = relationship("Renewal", back_populates="customer", cascade="all, delete-orphan")

    sales_activities = relationship("SalesActivity", back_populates="customer", cascade="all, delete-orphan")