from datetime import datetime, date
from enum import Enum
from sqlalchemy import String, Integer, ForeignKey, DateTime, Float, Enum as SqlEnum, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from mysite.database.db import Base


class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    delivered = "delivered"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    phone_number: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    registered_date: Mapped[date] = mapped_column(Date, default=date.today)
    user_token: Mapped[list["RefreshToken"]] = relationship("RefreshToken", back_populates="token_user", cascade="all, delete-orphan")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token: Mapped[str] = mapped_column(String, unique=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    token_user: Mapped["User"] = relationship("User", back_populates="user_token")


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String)
    store: Mapped[str] = mapped_column(String(150))
    product_name: Mapped[str] = mapped_column(String(150))
    price: Mapped[float] = mapped_column(Float)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[OrderStatus] = mapped_column(SqlEnum(OrderStatus), default=OrderStatus.pending)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)