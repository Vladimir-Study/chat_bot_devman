from asyncio.exceptions import TimeoutError
from asyncio import sleep
from aiohttp.client_exceptions import ClientConnectorError
from aiogram import Bot
from loguru import logger

import asyncio
import aiohttp
import argparse

from environs import Env

URLS = {
    "user_reviews": "https://dvmn.org/api/user_reviews/",
    "long_polling": "https://dvmn.org/api/long_polling/",
}

PARAMS = {"timeout": ""}


async def send_request_api_devman(
    url: str, headers: dict, params: dict | None = None
) -> dict:
    """
    Function send requests to the devman API.
    """
    timeout = aiohttp.ClientTimeout(total=90)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                logger.success("Devman request is success!")
                return await response.json()
            else:
                logger.info(
                    f"Devman request is not success! " f"Status code: {response.status}"
                )


async def send_notification_status_homework(
    url: str, headers: dict, chat_id: int, bot: Bot, params: dict | None = None
):
    """
    Function for long polling API Devman
    and send message in telegram
    """
    while True:
        try:
            devman_response = await send_request_api_devman(url, headers, params)
            if devman_response is not None:
                status = devman_response.get("status")
                if status == "found":
                    text_check_success = "Преподователю все понравилось, можно приступать к следующему уроку!"
                    text_check_error = "К сожалению в работе нашлись ошибки. "
                    check_status = devman_response.get("new_attempts")[0].get(
                        "is_negative"
                    )
                    message_text = f"""У Вас проверили работу "{devman_response.get('new_attempts')[0].get('lesson_title')}" 

{text_check_success if not check_status else text_check_error} Ссылка на урок: 
{devman_response.get('new_attempts')[0].get('lesson_url')}"""
                    await bot.delete_webhook(drop_pending_updates=True)
                    await bot.send_message(chat_id=chat_id, text=message_text)
                    params["timeout"] = devman_response.get("last_attempt_timestamp")
                    continue
                elif status == "timeout":
                    params["timeout"] = devman_response.get("timestamp_to_request")
                    continue
                else:
                    logger.error("LongPolling was been stopped.")
                    break
            else:
                logger.error("Devman return None")
                break
        except TimeoutError:
            logger.info("Refresh request after the timeout expires")
            continue
        except ClientConnectorError:
            logger.info("Refresh request after the connection failed")
            await sleep(30)
            continue
        except Exception as E:
            logger.error(f"Error from while cycle Devman request: {E}")
            break


async def main():
    env = Env()
    env.read_env()

    DEVMAN_TOKEN = env.str("TOKEN")
    BOT_TOKEN = env.str("BOT_TOKEN")

    parser = argparse.ArgumentParser()
    bot = Bot(BOT_TOKEN)


    headers = {"Authorization": f"Token {DEVMAN_TOKEN}"}

    logger.add(
        "./logs/log.log",
        rotation="1 day",
        colorize=True,
        compression="zip",
        format="{time} {level} {message}",
        encoding="utf-8",
    )

    parser.add_argument(
        "chat_id",
        type=int,
        help="Введите chat_id пользователя который будет получать уведомления: ",
    )

    args = parser.parse_args()
    chat_id = args.chat_id

    await send_notification_status_homework(
        URLS.get("long_polling"), headers, chat_id, bot, PARAMS
    )


if __name__ == "__main__":
    asyncio.run(main())
