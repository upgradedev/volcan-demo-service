"""Settings read from the environment once, when the app is created."""
import os
from dataclasses import dataclass

#: Browser front ends allowed to call this API.
DEFAULT_CORS_ORIGINS = ["*"]
DEFAULT_CORS_METHODS = ["GET", "POST", "PATCH", "DELETE"]


def _split(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    cors_origins: tuple[str, ...]
    cors_methods: tuple[str, ...]
    cors_allow_credentials: bool = True


def load_settings() -> Settings:
    origins = _split(os.getenv("CORS_ORIGINS", "")) or DEFAULT_CORS_ORIGINS
    methods = _split(os.getenv("CORS_METHODS", "")) or DEFAULT_CORS_METHODS
    return Settings(cors_origins=tuple(origins), cors_methods=tuple(methods))
