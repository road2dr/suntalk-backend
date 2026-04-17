from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, payments, auth, sendbird
from app.database import engine, Base
from app.models.models import User, Payment


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SunTalk Backend",
    description="SunTalk 채팅앱 관리 백엔드 API",
    version="1.0.0",
    servers=[{"url": "http://localhost:8000", "description": "개발 서버"}],
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(payments.router, prefix="/api")
app.include_router(sendbird.router, prefix="/api")


@app.get("/", tags=["Root"])
def root():
    return {"message": "SunTalk Backend API", "docs": "/docs"}


@app.get("/health", tags=["Root"])
def health():
    return {"status": "ok"}