from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./book_library.db"
    API_KEY: str = ''
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()