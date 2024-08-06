from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./book_library.db"
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()