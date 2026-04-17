from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"


class SnsLoginProvider(str, Enum):
    kakao = "kakao"
    naver = "naver"
    google = "google"
    apple = "apple"


class UserCreate(BaseModel):
    name: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[Gender] = None
    age: Optional[int] = None
    region_addr: Optional[str] = None
    kakao_id: Optional[str] = None
    naver_id: Optional[str] = None
    google_id: Optional[str] = None
    apple_id: Optional[str] = None
    thumbnail_url: Optional[str] = None
    background_image_url: Optional[str] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[Gender] = None
    age: Optional[int] = None
    region_addr: Optional[str] = None
    kakao_id: Optional[str] = None
    naver_id: Optional[str] = None
    google_id: Optional[str] = None
    apple_id: Optional[str] = None
    thumbnail_url: Optional[str] = None
    background_image_url: Optional[str] = None
    is_blocked: Optional[bool] = None
    points: Optional[int] = None


class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    nickname: Optional[str] = None
    gender: Optional[Gender] = None
    age: Optional[int] = None
    region_addr: Optional[str] = None
    thumbnail_url: Optional[str] = None
    background_image_url: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    name: str
    nickname: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    region_addr: Optional[str] = None
    kakao_id: Optional[str] = None
    naver_id: Optional[str] = None
    google_id: Optional[str] = None
    apple_id: Optional[str] = None
    thumbnail_url: Optional[str] = None
    background_image_url: Optional[str] = None
    points: int = 0
    is_blocked: bool = False
    login_completed: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int
    page: int
    page_size: int


class SnsLoginRequest(BaseModel):
    provider: SnsLoginProvider
    sns_id: str


class SnsLoginSuccessResponse(BaseModel):
    success: bool = True
    user: UserResponse
    message: str = "로그인에 성공했습니다."


class SnsLoginErrorResponse(BaseModel):
    success: bool = False
    error_code: int
    message: str