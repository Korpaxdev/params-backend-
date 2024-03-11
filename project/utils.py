from datetime import timedelta

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DB_NAME: str
    DB_USER: str
    DB_USER_PASSWORD: str
    DB_PORT: int
    DB_HOST: str = "localhost"
    ACCESS_TOKEN_LIFETIME_STR: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    @property
    def ACCESS_TOKEN_LIFETIME(self) -> timedelta:
        amount, unit = self.ACCESS_TOKEN_LIFETIME_STR.split()
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
        timedelta_setting = {unit_mapping[unit]: int(amount)}
        return timedelta(**timedelta_setting)
