from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    role = Column(String, nullable=False)

    customers = relationship("Customer", back_populates="assigned_rep")

    sales_activities = relationship("SalesActivity",back_populates="user",cascade="all, delete-orphan")

    opportunities = relationship("Opportunity",back_populates="owner",cascade="all, delete-orphan")