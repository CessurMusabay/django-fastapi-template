from .base import DEBUG, MIDDLEWARE
from .apps import INSTALLED_APPS

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

    INTERNAL_IPS = type("c", (), {"__contains__": lambda *a: True})()
