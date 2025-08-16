from enum import Enum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from .database import DatabaseSettings
from .domain import DomainSettings
from .cache import CacheSettings


class Settings(BaseSettings):
    debug: bool = True
    secret_key: SecretStr = "secret"
    version: str = "0.0.1"

    # JWT
    access_token_expire_days: int = 1
    refresh_token_expire_days: int = 7

    database: DatabaseSettings = DatabaseSettings()
    domain: DomainSettings = DomainSettings()
    cache: CacheSettings = CacheSettings()

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    @staticmethod
    def generate_env_file():
        from pydantic_core import PydanticUndefined
        from pydantic import BaseModel

        env_lines = []
        delimiter = Settings.model_config.get("env_nested_delimiter", "__")

        def _get_field_value(field_info):
            if field_info.default is not PydanticUndefined:
                return field_info.default
            if field_info.default_factory:
                return field_info.default_factory()
            return ""

        def _process_model_fields(model_cls, prefix=""):
            for field_name, field_info in model_cls.model_fields.items():
                env_var_name = f"{prefix}{field_name}".upper()

                if hasattr(field_info.annotation, "__mro__") and any(
                    issubclass(cls, (BaseSettings, BaseModel))
                    for cls in field_info.annotation.__mro__
                ):
                    _process_model_fields(
                        field_info.annotation, f"{env_var_name}{delimiter}"
                    )
                else:
                    value = _get_field_value(field_info)
                    if isinstance(value, SecretStr):
                        value = "your_secret_key_here"
                    elif isinstance(value, Enum):
                        value = value.value
                    elif isinstance(value, (list, dict)):
                        value = ""
                    env_lines.append(f"{env_var_name}={value}")

        _process_model_fields(Settings)

        env_content = "\n".join(env_lines)
        env_file_path = Path(__file__).parent.parent / ".env"
        with open(env_file_path, "w") as f:
            f.write(env_content)
        print(f"Generated .env file at: {env_file_path}")


settings = Settings()
