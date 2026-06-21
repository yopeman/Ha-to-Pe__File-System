from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str = 'sqlite:///db.sqlite3'

settings = Settings()