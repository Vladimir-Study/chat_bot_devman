from dataclasses import dataclass


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
