from pydantic_settings import BaseSettings


class DomainSettings(BaseSettings):
    domain: str = ""
    allowed_hosts: str = ""  # "127.0.0.1,localhost"
