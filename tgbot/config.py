from dataclasses import dataclass
from environs import Env

from tgbot.data.data import Data

@dataclass
class TgBot:
    token: str
    name: str
    version: str
    parse_mode: str


@dataclass
class Telethon:
    api_id: int
    api_hash: str


@dataclass
class Log:
    enter_start: bool
    enter_phone: bool
    get_session: bool
    invalid_session: bool
    reset_auth: bool


@dataclass
class Config:
    bot: TgBot
    data: Data
    admin: int

    use_proxy: bool
    check_valid_session: int
    spam_in_connect_session: bool
    spam_in_reset_auth: bool
    find_chats: list
    auto_check_passwords: bool

    telegram: Telethon
    log: Log
    


def load_config(path: str):
    env = Env()
    env.read_env(path)

    return Config(
        bot=TgBot(
            token=env.str('BOT_TOKEN'),
            name=env.str('BOT_NAME'),
            version=env.str('BOT_VERSION'),
            parse_mode=env.str('BOT_PARSE_MODE')
        ),
        data=Data().load(),
        admin=env.int('ADMIN_ID'),
        use_proxy=env.bool('USE_PROXY'),
        check_valid_session=env.int('CHECK_VALID_SESSION'),
        spam_in_connect_session=env.bool('SPAM_IN_CONNECT_SESSION'),
        spam_in_reset_auth=env.bool('SPAM_IN_RESET_AUTH'),
        auto_check_passwords=env.bool('AUTO_CHECH_PASSWORDS'),
        telegram=Telethon(
            api_id=env.int('TELEGRAM_API_ID'),
            api_hash=env.str('TELEGRAM_API_HASH')
        ),
        log=Log(
            enter_start=env.bool('LOG_ENTER_START'),
            enter_phone=env.bool('LOG_ENTER_PHONE'),
            get_session=env.bool('LOG_GET_SESSION'),
            reset_auth=env.bool('LOG_RESET_AUTH'),
            invalid_session=env.bool('LOG_INVALID_SESSION')
        ),
        find_chats=env.list('FIND_CHATS')
    )
