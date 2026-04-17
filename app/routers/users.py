from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
import httpx
from sqlalchemy.orm import Session
from sqlalchemy import func as sa_func
from app.database import get_db
from app.models.models import User
from app.config import settings
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserProfileUpdate,
    UserResponse,
    UserListResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


def _enrich_user(user: User) -> dict:
    user_dict = _user_to_dict(user)
    has_email = bool(user.email)
    user_dict["login_completed"] = has_email
    return user_dict


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


async def _fetch_sendbird_user(user_id: str) -> Optional[dict]:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"https://api-{settings.SENDBIRD_APP_ID}.sendbird.com/v3/users/{user_id}",
                headers={"Api-Token": settings.SENDBIRD_API_TOKEN},
            )
            if response.status_code == 200:
                return response.json()
    except Exception:
        pass
    return None


def _merge_sendbird(user_data: dict, sb_data: Optional[dict]) -> dict:
    if not sb_data:
        return user_data
    sb = sb_data.get("nickname", "") or ""
    if sb and not user_data.get("nickname"):
        user_data["nickname"] = sb
    sb_profile = sb_data.get("profile_url", "") or ""
    if sb_profile and not user_data.get("thumbnail_url"):
        user_data["thumbnail_url"] = sb_profile
    return user_data


@router.get("/", response_model=UserListResponse, summary="사용자 목록 조회")
def get_users(
    page: int = Query(1, ge=1, description="페이지 번호"),
    page_size: int = Query(20, ge=1, le=100, description="페이지 크기"),
    name: Optional[str] = Query(None, description="이름 검색"),
    email: Optional[str] = Query(None, description="이메일 검색"),
    db: Session = Depends(get_db),
):
    query = db.query(User)

    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    total = query.count()
    users = query.offset((page - 1) * page_size).limit(page_size).all()

    enriched = [_enrich_user(u) for u in users]

    return UserListResponse(
        users=[UserResponse(**u) for u in enriched],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{user_id}", response_model=UserResponse, summary="사용자 상세 조회")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    user_dict = _enrich_user(user)

    sb_data = await _fetch_sendbird_user(user_id)
    user_dict = _merge_sendbird(user_dict, sb_data)

    return UserResponse(**user_dict)


@router.post("/", response_model=UserResponse, status_code=201, summary="사용자 생성")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump(exclude_none=True))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user_data = _enrich_user(db_user)
    return UserResponse(**user_data)


@router.patch("/{user_id}", response_model=UserResponse, summary="사용자 정보 수정 (관리자)")
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    update_data = user.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    user_data = _enrich_user(db_user)
    return UserResponse(**user_data)


@router.patch("/{user_id}/profile", response_model=UserResponse, summary="사용자 프로필 업데이트")
def update_profile(user_id: str, profile: UserProfileUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    update_data = profile.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    user_data = _enrich_user(db_user)
    return UserResponse(**user_data)


@router.patch("/{user_id}/block", response_model=UserResponse, summary="사용자 차단/차단해제")
def toggle_block_user(user_id: str, is_blocked: bool, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    db_user.is_blocked = is_blocked
    db.commit()
    db.refresh(db_user)
    user_data = _enrich_user(db_user)
    return UserResponse(**user_data)


@router.delete("/{user_id}", status_code=204, summary="사용자 삭제")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return None