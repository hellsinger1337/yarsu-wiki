from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    database_url: str
    yandex_smtp_server: str
    yandex_smtp_port: int
    yandex_email: str
    yandex_password: str

    class Config:
        env_file = ".env"

settings = Settings()
