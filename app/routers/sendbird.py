from fastapi import APIRouter, HTTPException
import httpx
from app.config import settings

router = APIRouter(prefix="/sendbird", tags=["Sendbird"])


@router.get("/users/{user_id}", summary="Sendbird 사용자 정보 조회")
async def get_sendbird_user(user_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api-{settings.SENDBIRD_APP_ID}.sendbird.com/v3/users/{user_id}",
            headers={"Api-Token": settings.SENDBIRD_API_TOKEN},
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Sendbird 사용자 조회 실패")
    return response.json()


@router.post("/users", summary="Sendbird 사용자 생성")
async def create_sendbird_user(user_id: str, nickname: str, profile_url: str = ""):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api-{settings.SENDBIRD_APP_ID}.sendbird.com/v3/users",
            headers={"Api-Token": settings.SENDBIRD_API_TOKEN},
            json={
                "user_id": user_id,
                "nickname": nickname,
                "profile_url": profile_url,
            },
        )
    if response.status_code not in (200, 201):
        raise HTTPException(status_code=response.status_code, detail="Sendbird 사용자 생성 실패")
    return response.json()


@router.delete("/users/{user_id}", summary="Sendbird 사용자 삭제")
async def delete_sendbird_user(user_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"https://api-{settings.SENDBIRD_APP_ID}.sendbird.com/v3/users/{user_id}",
            headers={"Api-Token": settings.SENDBIRD_API_TOKEN},
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Sendbird 사용자 삭제 실패")
    return {"message": "삭제 완료"}


@router.post("/users/{user_id}/block", summary="Sendbird 사용자 차단")
async def block_sendbird_user(user_id: str, blocked_user_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api-{settings.SENDBIRD_APP_ID}.sendbird.com/v3/users/{user_id}/block",
            headers={"Api-Token": settings.SENDBIRD_API_TOKEN},
            json={"blocked_user_id": blocked_user_id},
        )
    if response.status_code not in (200, 201):
        raise HTTPException(status_code=response.status_code, detail="Sendbird 사용자 차단 실패")
    return response.json()