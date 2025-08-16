from enum import Enum

from pydantic_settings import BaseSettings


class CacheTypes(Enum):
    redis = "redis"
    memory = "memory"
    dummy = "dummy"


class CacheSettings(BaseSettings):
    cache_enabled: bool = True
    cache_type: CacheTypes = CacheTypes.memory
    redis_password: str = ""
