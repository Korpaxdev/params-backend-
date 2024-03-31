from datetime import timedelta

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from rest_framework import serializers


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DB_NAME: str
    DB_USER: str
    DB_USER_PASSWORD: str
    DB_PORT: int
    DB_HOST: str = "localhost"
    ACCESS_TOKEN_LIFETIME_STR: str
    PASSWORD_RESET_TOKEN_LIFETIME_STR: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_HOST_USER: EmailStr
    EMAIL_HOST_PASSWORD: str
    ALLOWED_HOSTS: list[str]

    @property
    def ACCESS_TOKEN_LIFETIME(self) -> timedelta:
        return map_str_to_timedelta(self.ACCESS_TOKEN_LIFETIME_STR)

    @property
    def PASSWORD_RESET_TOKEN_LIFETIME(self) -> timedelta:
        return map_str_to_timedelta(self.PASSWORD_RESET_TOKEN_LIFETIME_STR)


def map_str_to_timedelta(date_str: str) -> timedelta:
    unit_mapping = {
        "days": "days",
        "day": "days",
        "hours": "hours",
        "hour": "hours",
        "minutes": "minutes",
        "minute": "minutes",
        "seconds": "seconds",
        "second": "seconds",
    }
    amount, unit = date_str.split()
    return timedelta(**{unit_mapping[unit]: int(amount)})


def serializer_validate_password(password: str) -> str:
    try:
        validate_password(password)
    except ValidationError as error:
        raise serializers.ValidationError(detail=error.messages)
    return password
