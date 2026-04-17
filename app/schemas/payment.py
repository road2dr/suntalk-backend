from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class PaymentMethod(str, Enum):
    card = "card"
    kakao_pay = "kakao_pay"
    naver_pay = "naver_pay"
    apple_pay = "apple_pay"
    google_pay = "google_pay"
    bank_transfer = "bank_transfer"
    other = "other"


class PaymentPurpose(str, Enum):
    subscription = "subscription"
    item_purchase = "item_purchase"
    gift = "gift"
    donation = "donation"
    coin_purchase = "coin_purchase"
    other = "other"


class PaymentCreate(BaseModel):
    user_id: str
    amount: int
    payment_method: PaymentMethod
    purpose: PaymentPurpose
    description: Optional[str] = None
    points_rate: Optional[float] = None


class PaymentUpdate(BaseModel):
    amount: Optional[int] = None
    payment_method: Optional[PaymentMethod] = None
    purpose: Optional[PaymentPurpose] = None
    description: Optional[str] = None
    status: Optional[str] = None


class PaymentResponse(BaseModel):
    id: str
    user_id: str
    amount: int
    points_earned: int = 0
    payment_method: str
    purpose: str
    description: Optional[str] = None
    status: str = "completed"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PaymentWithUserResponse(PaymentResponse):
    user_name: Optional[str] = None
    user_nickname: Optional[str] = None
    user_email: Optional[str] = None


class PaymentListResponse(BaseModel):
    payments: list[PaymentWithUserResponse]
    total: int
    page: int
    page_size: int