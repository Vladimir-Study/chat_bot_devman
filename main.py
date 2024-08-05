from asyncio.exceptions import TimeoutError
from environs import Env
from config import logger

import asyncio
import aiohttp

env = Env()
env.read_env()

urls = {
    "user_reviews": "https://dvmn.org/api/user_reviews/",
    "long_polling": "https://dvmn.org/api/long_polling/",
}

headers = {
    "Authorization": f"Token {env.str('TOKEN')}"
}

params = {
    "timeout": "1722839837.685598"
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
            if isinstance(response, dict):
                params['timeout'] = response.get("last_attempt_timestamp")
                continue
            else:
                break
        except TimeoutError:
            logger.info("Refresh request after the timeout expires")
            continue
        except Exception as E:
            logger.error(f"Error from while cycle Devman request: {E}")
            break


async def main():
    await long_polling_request(urls.get("long_polling"), headers, params)

if __name__ == "__main__":
    asyncio.run(main())