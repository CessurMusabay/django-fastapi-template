from .base import DEBUG, BASE_DIR
import os
from config import settings


cache_mapping = {
    "redis": {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"redis://:{settings.cache.redis_password}@redis:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    },
    "memory": {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    },
    "dummy": {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    },
}


CACHES = cache_mapping.get(settings.cache.cache_type.value)

if not settings.cache.cache_enabled:
    CACHES = cache_mapping.get("dummy")
