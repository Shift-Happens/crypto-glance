from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Crypto Glance API"
    aws_region: str = "eu-central-1"
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_sender: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
