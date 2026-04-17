# SunTalk Backend

SunTalk 채팅앱 관리 백엔드 API (FastAPI + MySQL + Sendbird)
Suntalk Made with opencode

## 로컬 개발

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload --port 8000

# 테스트
python -m pytest tests/ -v
```

## Docker 배포

### 1. 서버 준비 (네이버 클라우드 플랫폼)

```bash
# Ubuntu 서버에 Docker 설치
curl -fsSL https://get.docker.com | sh
sudo apt install -y docker-compose-plugin
```

### 2. 저장소 클론

```bash
cd /opt
git clone https://github.com/road2dr/suntalk-backend.git
git clone https://github.com/road2dr/suntalk-admin.git
```

### 3. 환경변수 설정

```bash
cd /opt/suntalk-backend
cat > .env << 'EOF'
MYSQL_ROOT_PASSWORD=변경하세요
MYSQL_PASSWORD=변경하세요
SENDBIRD_APP_ID=DFE7328E-97B5-402A-B9A4-3B410605296B
SENDBIRD_API_TOKEN=your_token
ADMIN_USERNAME=admin
ADMIN_PASSWORD=변경하세요
EOF
```

### 4. 실행

```bash
cd /opt/suntalk-backend
docker compose up -d
```

### 5. 접속

- Admin UI: `http://<서버IP>/`
- API Swagger: `http://<서버IP>:8000/docs`
- MySQL: `<서버IP>:3306`

### 6. ACG (방화벽) 설정

네이버 클라우드 콘솔 > Security > ACG에서 다음 inbound 규칙 추가:

| 포트 | 프로토콜 | 접근 소스 | 설명 |
|------|----------|-----------|------|
| 22 | TCP | 관리 IP만 | SSH |
| 80 | TCP | 0.0.0.0/0 | Admin UI |
| 8000 | TCP | 0.0.0.0/0 | API (선택) |

### 7. 업데이트

```bash
cd /opt/suntalk-backend && git pull
cd /opt/suntalk-admin && git pull
cd /opt/suntalk-backend && docker compose up -d --build
```