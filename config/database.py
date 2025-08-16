from pydantic_settings import BaseSettings


from enum import Enum


class DatabaseTypes(str, Enum):
    sqlite = "sqlite"
    postgres = "postgres"


class DatabaseSettings(BaseSettings):
    name: str = ""
    host: str = ""
    port: int = 5432
    user: str = ""
    password: str = ""
    type: DatabaseTypes = DatabaseTypes.sqlite
