from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User, Payment
from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse,
    PaymentWithUserResponse,
    PaymentListResponse,
)

router = APIRouter(prefix="/payments", tags=["Payments"])

DEFAULT_POINTS_RATE = 0.1


def _payment_to_dict(p: Payment) -> dict:
    return {
        "id": p.id,
        "user_id": p.user_id,
        "amount": p.amount,
        "points_earned": p.points_earned,
        "payment_method": p.payment_method,
        "purpose": p.purpose,
        "description": p.description,
        "status": p.status,
        "created_at": p.created_at,
        "updated_at": p.updated_at,
    }


@router.get("/", response_model=PaymentListResponse, summary="결제 목록 조회")
def get_payments(
    page: int = Query(1, ge=1, description="페이지 번호"),
    page_size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    user_id: Optional[str] = Query(None, description="사용자 ID 필터"),
    payment_method: Optional[str] = Query(None, description="결제 수단 필터"),
    purpose: Optional[str] = Query(None, description="결제 용도 필터"),
    start_date: Optional[datetime] = Query(None, description="시작일 필터"),
    end_date: Optional[datetime] = Query(None, description="종료일 필터"),
    db: Session = Depends(get_db),
):
    query = db.query(Payment).join(User, Payment.user_id == User.id)

    if user_id:
        query = query.filter(Payment.user_id == user_id)
    if payment_method:
        query = query.filter(Payment.payment_method == payment_method)
    if purpose:
        query = query.filter(Payment.purpose == purpose)
    if start_date:
        query = query.filter(Payment.created_at >= start_date)
    if end_date:
        query = query.filter(Payment.created_at <= end_date)

    total = query.count()
    payments = query.order_by(Payment.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    result = []
    for p in payments:
        p_dict = _payment_to_dict(p)
        result.append(
            PaymentWithUserResponse(
                **p_dict,
                user_name=p.user.name if p.user else None,
                user_nickname=p.user.nickname if p.user else None,
                user_email=p.user.email if p.user else None,
            )
        )

    return PaymentListResponse(
        payments=result,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{payment_id}", response_model=PaymentWithUserResponse, summary="결제 상세 조회")
def get_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="결제 정보를 찾을 수 없습니다.")

    p_dict = _payment_to_dict(payment)
    return PaymentWithUserResponse(
        **p_dict,
        user_name=payment.user.name if payment.user else None,
        user_nickname=payment.user.nickname if payment.user else None,
        user_email=payment.user.email if payment.user else None,
    )


@router.post("/", response_model=PaymentResponse, status_code=201, summary="결제 정보 생성")
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payment.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    points_rate = payment.points_rate if payment.points_rate is not None else DEFAULT_POINTS_RATE
    points_earned = int(payment.amount * points_rate)

    db_payment = Payment(
        **payment.model_dump(exclude_none=True, exclude={"points_rate"}),
        points_earned=points_earned,
    )
    db.add(db_payment)

    user.points = (user.points or 0) + points_earned
    db.commit()
    db.refresh(db_payment)

    return PaymentResponse(**_payment_to_dict(db_payment))


@router.patch("/{payment_id}", response_model=PaymentResponse, summary="결제 정보 수정")
def update_payment(payment_id: str, payment: PaymentUpdate, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="결제 정보를 찾을 수 없습니다.")

    update_data = payment.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(db_payment, key, value)

    db.commit()
    db.refresh(db_payment)
    return PaymentResponse(**_payment_to_dict(db_payment))


@router.delete("/{payment_id}", status_code=204, summary="결제 정보 삭제")
def delete_payment(payment_id: str, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if db_payment:
        db.delete(db_payment)
        db.commit()
    return None