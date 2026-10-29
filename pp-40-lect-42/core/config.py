from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = 'E-commerce APP'
    debug: bool = False
    database_url: str
    secret_key: str
    algorithm: str = 'HS256'
    access_token_expires_minutes: int = 15
    refresh_token_expires_days: int = 7

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
