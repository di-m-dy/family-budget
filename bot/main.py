"""
Main module for bot app
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from core.config import settings
from bot.handlers import router

logging.basicConfig(level=logging.INFO)


bot = Bot(token=settings.tg_token)
dp = Dispatcher()

dp.include_router(router)


async def start_bot():
    logging.info("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())
