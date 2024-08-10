from config import config
from aiogram import Bot, Dispatcher

bot = Bot(config.tg_bot.bot_token)
dp = Dispatcher()


async def process_send_success_notification(chat_id: int, message_text: str) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.send_message(chat_id=chat_id, text=message_text)
