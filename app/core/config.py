from pydantic_settings import BaseSettings, SettingsConfigDict
   
from app.core.logging import logger

    
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    PORT: int
    HOST: str
    DEBUG: bool

    DATA_FILEPATH: str
    SLIDING_WINDOW: int
    FLUSH_INTERVAL: int
    FLUSH_COUNT: int
    
settings = Settings()