from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str = 'sqlite:///db.sqlite3'
    secret_key: str = 'sdlkfh sldijsl;l ;aslxkma zxnm,zcb wioejla aksj'

settings = Settings()