from loguru import logger
from dataclasses import dataclass


logger.add(
    "./logs/log.log",
    rotation="1 day",
    colorize=True,
    compression="zip",
    format="{time} {level} {message}",
    encoding="utf-8",
)


@dataclass
class DevmanConfig:
    token: str


@dataclass
class BotConfig:
    bot_token: str


@dataclass
class UserData:
    tg_uid: int


@dataclass
class Config:
    devman_config: DevmanConfig
    tg_bot: BotConfig
    user_data: UserData
