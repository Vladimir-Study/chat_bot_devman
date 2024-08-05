from environs import Env
from config import logger
from pprint import pprint

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
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    logger.success("Devman request is success!")
                    return await response.json()
                else:
                    logger.info(f"Devman request is not success! "
                                f"Status code: {response.status}")
    except Exception as E:
        logger.error(f"Error from Devman request: {E}")


async def main():
    while True:
        try:
            response = await devman_api_requests(urls.get("long_polling"), headers, params)
            pprint(response)
            if isinstance(response, dict):
                params['timeout'] = response.get("last_attempt_timestamp")
                continue
            else:
                break
        except Exception as E:
            logger.error(f"Error from while cycle Devman request: {E}")
            break


if __name__ == "__main__":
    asyncio.run(main())