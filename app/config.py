from pydantic import BaseSettings

class Settings(BaseSettings):
    db_uri: str
    db_name: str
    redis_host: str
    redis_port: int
    redis_cache_ttl: int

    class Config:
        env_file = '.env'


settings = Settings()