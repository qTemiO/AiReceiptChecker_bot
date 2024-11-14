from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.joinpath(".env").__str__())
    # Service configs
    BOT_TOKEN: str

settings = Settings()