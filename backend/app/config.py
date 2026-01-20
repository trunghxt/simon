from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_DB_NAME: str = "simon_math"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    PROJECT_NAME: str = "Simon Math API"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
