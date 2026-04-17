from sqlalchemy import Column, String, Integer, BigInteger, Boolean, Enum, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    nickname = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    gender = Column(Enum("male", "female", "other"), nullable=True)
    age = Column(Integer, nullable=True)
    region_addr = Column(String(500), nullable=True)
    kakao_id = Column(String(255), nullable=True, unique=True)
    naver_id = Column(String(255), nullable=True, unique=True)
    google_id = Column(String(255), nullable=True, unique=True)
    apple_id = Column(String(255), nullable=True, unique=True)
    thumbnail_url = Column(Text, nullable=True)
    background_image_url = Column(Text, nullable=True)
    points = Column(BigInteger, default=0)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)
    points_earned = Column(Integer, default=0)
    payment_method = Column(
        Enum("card", "kakao_pay", "naver_pay", "apple_pay", "google_pay", "bank_transfer", "other"),
        nullable=False,
    )
    purpose = Column(
        Enum("subscription", "item_purchase", "gift", "donation", "coin_purchase", "other"),
        nullable=False,
    )
    description = Column(Text, nullable=True)
    status = Column(
        Enum("pending", "completed", "failed", "refunded"),
        default="completed",
    )
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="payments")