from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=1000)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    expenses = relationship("Expense", back_populates="user")
    categories = relationship("Category", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    expenses = relationship("Expense", back_populates="category")
    user = relationship("User", back_populates="categories")


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    category = relationship("Category", back_populates="expenses")
    user = relationship("User", back_populates="expenses")