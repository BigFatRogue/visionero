from pydantic_settings import BaseSettings, SettingsConfigDict
   
    
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATA_FILEPATH: str
    SLIDING_WINDOW: int
    FLUSH_INTERVAL: int
    FLUSH_COUNT: int
    

settings = Settings()