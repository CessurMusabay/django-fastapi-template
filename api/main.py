import os
import django
from fastapi import FastAPI, APIRouter
from django.core.asgi import get_asgi_application

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from config import settings
from api.auth.router import router as auth_router
from example_app.api.router import router as example_app_router

app = FastAPI(
    title="My Api",
    debug=settings.debug,
    docs_url="/api/docs" if settings.debug else None,
    redoc_url="/api/redoc" if settings.debug else None,
    openapi_url="/api/openapi.json" if settings.debug else None,
    version=settings.version,
)

# API Routers
api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(example_app_router, prefix="/example-app")

app.include_router(api_router)


# Get the Django ASGI app and mount it
django_app = get_asgi_application()
app.mount("", django_app)
