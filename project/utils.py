from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DB_NAME: str
    DB_USER: str
    DB_USER_PASSWORD: str
    DB_PORT: int
    DB_HOST: str = "localhost"
