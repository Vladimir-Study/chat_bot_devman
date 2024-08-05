from loguru import logger

logger.add("./logs/log.log", rotation="1 day", colorize=True, compression="zip",
           format="{time} {level} {message}", encoding="utf-8")