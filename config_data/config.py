from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    payment_provider_token: str | None
    database_url: str


@dataclass
class Config:
    """
    Класс с конфигурацией 
    """
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env("TELEGRAM_TOKEN"),
            payment_provider_token=env("PAYMENT_PROVIDER_TOKEN"),
            database_url=env("DATABASE_URL")
        )
    )
