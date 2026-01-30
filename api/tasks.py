"""
Tasks module for asynchronous operations.
"""

import json
import logging

from parser.utils import parse_invoice
from api.telegram_utils import send_telegram_message
from core.config import redis
from bot.keyboards import web_app_invoice


logger = logging.getLogger(__name__)

async def invoice_to_telegram_bot(url: str, chat_id: int):
    """
    Task to parse invoice and send data to Telegram bot.
    """
    try:
        parsed_data = parse_invoice(url)

        amount = parsed_data.get('amount')
        place = parsed_data.get('place')
        address = parsed_data.get('address')
        date = parsed_data.get('date')
        items = parsed_data.get("items", [])
        


        if 'iic=' in url:
            iic_split = url.split('iic=')
            iic = iic_split[1].split('&')[0]
        else:
            iic = None

        if not (date, items):
            logger.error("No date or items at data invoice")
            await send_telegram_message(chat_id=chat_id, text="Не удалось распознать чек")
            return
        
        # save to redis
        try:
            if iic:
                await redis.set("invoice:%s" % iic, json.dumps(parsed_data))
            else:
                await send_telegram_message(chat_id=chat_id, text="Не удалось сохранить чек в базу, отсутствует идентификатор")
        except Exception as e:
            logger.error("Error with adding to redis: %s" % e)
            await send_telegram_message(chat_id=chat_id, text="Не удалось добавить данные в базу")

        if items:
            items_str = "\n".join([f"- {item['title']}: {item['price']}" for item in items])
        else:
            items_str = "Нет товаров."
        message_header = f"Чек:\nПотрачено: {amount}\nМесто: {place}\nАдрес: {address}\nДата: {date}\n\n"
        message_content = "Товары:\n" if items else "Товары отсутствуют."
        message = message_header + message_content + items_str
        await send_telegram_message(chat_id, message, reply_markup=web_app_invoice(iic))
        logger.info(f"Sent invoice data to chat_id {chat_id}")
    except Exception as e:
        logger.error(f"Error in invoice_to_telegram_bot task: {e}")
        raise e
