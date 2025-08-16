from .base import DEBUG, BASE_DIR, MIDDLEWARE


MIDDLEWARE.append(
    "django_user_agents.middleware.UserAgentMiddleware",
)
