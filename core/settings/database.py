from .base import BASE_DIR
from config import settings


db_mapping = {
    "sqlite": {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    },
    "postgres": {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": settings.database.name,
            "USER": settings.database.user,
            "PASSWORD": settings.database.password,
            "HOST": settings.database.host,
            "PORT": settings.database.port,
        }
    },
}


DATABASES = db_mapping.get(settings.database.type.value)
