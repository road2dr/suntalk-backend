import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "suntalk")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "suntalk123")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "suntalk")

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )

    SENDBIRD_APP_ID: str = os.getenv("SENDBIRD_APP_ID", "")
    SENDBIRD_API_TOKEN: str = os.getenv("SENDBIRD_API_TOKEN", "")
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")


settings = Settings()