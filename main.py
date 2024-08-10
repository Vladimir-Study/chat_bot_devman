from asyncio.exceptions import TimeoutError
from asyncio import sleep
from aiohttp.client_exceptions import ClientConnectorError
from pprint import pprint

from bot import process_send_success_notification
from config import config


import asyncio
import aiohttp

logger = config.logger.logger

urls = {
    "user_reviews": "https://dvmn.org/api/user_reviews/",
    "long_polling": "https://dvmn.org/api/long_polling/",
}

headers = {
    "Authorization": f"Token {config.devman_config.token}"
}

params = {
    "timeout": "1722839837"
}


async def devman_api_requests(url: str, headers: dict, params: dict | None = None) -> dict:
    '''
    Function get requests to the devman API.
    '''
    timeout = aiohttp.ClientTimeout(total=90)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                logger.success("Devman request is success!")
                return await response.json()
            else:
                logger.info(f"Devman request is not success! "
                            f"Status code: {response.status}")


async def long_polling_request(url: str, headers: dict, params: dict | None = None):
    '''
    Function for long polling API Devman
    '''
    while True:
        try:
            response = await devman_api_requests(url, headers, params)
            status = response.get("status")
            if status == "found":
                text_check_success = "Преподователю все понравилось, " \
                                     "можно приступать к следующему уроку!"
                text_check_error = "К сожалению в работе нашлись ошибки."
                text_notification = f"У Вас проверили работу " \
                                    f"\"{response.get('new_attempts')[0].get('lesson_title')}\" \n\n"
                text_lesson_url = f"Ссылка на урок: {response.get('new_attempts')[0].get('lesson_url')}"
                check_status = response.get('new_attempts')[0].get('is_negative')
                message_text = f"{text_notification} " \
                               f"{text_check_success if not check_status else text_check_error} " \
                               f"{text_lesson_url}"
                await process_send_success_notification(message_text)
                params['timeout'] = response.get("last_attempt_timestamp")
                continue
            elif status == "timeout":
                params['timeout'] = response.get("timestamp_to_request")
                continue
            else:
                logger.error("LongPolling was been stopped.")
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
    await long_polling_request(urls.get("long_polling"), headers, params)
    # response = await devman_api_requests(urls.get("user_reviews"), headers)
    # pprint(response)

if __name__ == "__main__":
    asyncio.run(main())