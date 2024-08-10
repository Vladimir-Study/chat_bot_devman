from loguru import logger
from loguru._logger import Logger
from dataclasses import dataclass
from environs import Env


env = Env()
env.read_env()


logger.add("./logs/log.log", rotation="1 day", colorize=True, compression="zip",
           format="{time} {level} {message}", encoding="utf-8")


@dataclass
class DevmanConfig:
    token: str


@dataclass
class MyLogger:
    logger: Logger


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
    logger: MyLogger
    user_data: UserData


config = Config(
    devman_config=DevmanConfig(token=env.str('TOKEN')),
    tg_bot=BotConfig(bot_token=env("BOT_TOKEN")),
    logger=MyLogger(logger=logger),
    user_data=UserData(tg_uid=env.int("TG_UID"))
)