from datetime import datetime, date
<<<<<<< HEAD
from typing import List
from enum import Enum as PyEnum
from sqlalchemy import String, DateTime, Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SqlEnum
=======
from enum import Enum

from sqlalchemy import String, Integer, ForeignKey, DateTime, Float, Enum as SqlEnum, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
>>>>>>> 79752a4 (chain)

from mysite.database.db import Base


<<<<<<< HEAD
class Status(str, PyEnum):
    basic = "basic"
    pro = "pro"


class UserProfile(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    status: Mapped[Status] = mapped_column(SqlEnum(Status), default=Status.basic)
    registered_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_token: Mapped[List["RefreshToken"]] = relationship("RefreshToken",back_populates="token_user",cascade="all, delete-orphan")
    user_file: Mapped[List["FileObject"]] = relationship("FileObject", back_populates="user", cascade="all, delete-orphan")
=======
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
>>>>>>> 79752a4 (chain)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token: Mapped[str] = mapped_column(String, unique=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

<<<<<<< HEAD
    token_user: Mapped["UserProfile"] = relationship("UserProfile",back_populates="user_token")


class DailyUsage(Base):
    __tablename__ = "daily_usage"
    __table_args__ = (UniqueConstraint("user_id", "usage_date", name="uq_user_daily_usage"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    usage_date: Mapped[date] = mapped_column(Date, default=date.today)
    messages_used: Mapped[int] = mapped_column(Integer, default=0)
    images_used: Mapped[int] = mapped_column(Integer, default=0)


class FileObject(Base):
    __tablename__ = "file_object"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dataset_file: Mapped[str] = mapped_column(String)
    task_file: Mapped[str | None] = mapped_column(String, nullable=True)
    img_file: Mapped[str | None] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user_file")
=======
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
>>>>>>> 79752a4 (chain)
