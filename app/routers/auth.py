from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User
from app.config import settings
from app.schemas.user import (
    SnsLoginRequest,
    SnsLoginSuccessResponse,
    SnsLoginErrorResponse,
    UserResponse,
    SnsLoginProvider,
)

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBasic()


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


ERROR_USER_NOT_FOUND = 1001
ERROR_USER_BLOCKED = 1002
ERROR_INVALID_PROVIDER = 1003
ERROR_LOGIN_INCOMPLETE = 1004

SNS_ID_FIELD_MAP = {
    SnsLoginProvider.kakao: "kakao_id",
    SnsLoginProvider.naver: "naver_id",
    SnsLoginProvider.google: "google_id",
    SnsLoginProvider.apple: "apple_id",
}


@router.post("/login", response_model=AdminLoginResponse, summary="관리자 로그인")
def admin_login(req: AdminLoginRequest):
    if (
        req.username == settings.ADMIN_USERNAME
        and req.password == settings.ADMIN_PASSWORD
    ):
        token = secrets.token_urlsafe(32)
        return AdminLoginResponse(access_token=token)
    raise HTTPException(status_code=401, detail="인증 정보가 올바르지 않습니다.")


@router.post("/verify", summary="토큰 검증")
def verify_token(credentials: HTTPBasicCredentials = Depends(security)):
    if (
        credentials.username == settings.ADMIN_USERNAME
        and credentials.password == settings.ADMIN_PASSWORD
    ):
        return {"valid": True}
    raise HTTPException(status_code=401, detail="인증 정보가 올바르지 않습니다.")


@router.post("/sns-login", summary="SNS 계정 로그인")
def sns_login(req: SnsLoginRequest, db: Session = Depends(get_db)):
    field = SNS_ID_FIELD_MAP.get(req.provider)
    if not field:
        return SnsLoginErrorResponse(
            error_code=ERROR_INVALID_PROVIDER,
            message=f"지원하지 않는 로그인 제공자입니다: {req.provider}",
        )

    user = db.query(User).filter(getattr(User, field) == req.sns_id).first()

    if not user:
        return SnsLoginErrorResponse(
            error_code=ERROR_USER_NOT_FOUND,
            message="해당 SNS 계정으로 등록된 사용자가 없습니다.",
        )

    if user.is_blocked:
        return SnsLoginErrorResponse(
            error_code=ERROR_USER_BLOCKED,
            message="차단된 계정입니다.",
        )

    has_email = bool(user.email)
    user_dict = _user_to_dict(user)
    user_dict["login_completed"] = has_email

    if not has_email:
        return SnsLoginErrorResponse(
            error_code=ERROR_LOGIN_INCOMPLETE,
            message="이메일 정보가 없어 로그인이 완료되지 않았습니다.",
        )

    return SnsLoginSuccessResponse(
        user=UserResponse(**user_dict),
        message="로그인에 성공했습니다.",
    )


def _user_to_dict(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "nickname": user.nickname,
        "email": user.email,
        "gender": user.gender,
        "age": user.age,
        "region_addr": user.region_addr,
        "kakao_id": user.kakao_id,
        "naver_id": user.naver_id,
        "google_id": user.google_id,
        "apple_id": user.apple_id,
        "thumbnail_url": user.thumbnail_url,
        "background_image_url": user.background_image_url,
        "points": user.points,
        "is_blocked": user.is_blocked,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }