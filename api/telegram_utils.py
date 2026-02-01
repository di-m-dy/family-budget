"""
Module for Telegram utility functions.
"""

import logging

from bot.main import bot

logger = logging.getLogger(__name__)


async def send_telegram_message(chat_id: int, text: str, reply_markup=None):
    """
    Send a message via Telegram bot
    """
    try:
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Failed to send message to {chat_id}: {e}")
        raise e
