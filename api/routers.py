"""
Module for FastAPI routers.
"""

import datetime
import json
import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, status

from api.schemas import DataToSheet, InvoiceToSheet, ParseInvoiceUrl, SendMessageRequest
from api.tasks import invoice_to_telegram_bot
from api.telegram_utils import send_telegram_message
from core.config import redis
from google_services.utils import append_value_sheet

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/ping")
async def ping_rt():
    """
    Ping router for health check
    """
    logger.info("Ping request received")
    return {"message": "pong"}


@router.post("/send_message")
async def send_message_rt(data: SendMessageRequest):
    """
    Send a message via Telegram bot
    """
    try:
        await send_telegram_message(data.chat_id, data.text)
        logger.info(f"Message sent to chat_id {data.chat_id}")
        return {"message": "Message from %s with sent: %s" % (data.chat_id, data.text)}
    except Exception as e:
        logger.error(f"Error sending message to chat_id {data.chat_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/save_to_sheet")
async def save_to_sheet_rt(data: DataToSheet):
    """
    Save data to Google Sheet
    """
    logger.info(data.date)
    try:
        result = append_value_sheet(
            date=data.date,
            amount=data.amount,
            category=data.category,
            note=data.type,
        )
        logger.info(f"Data to be saved to sheet: {data}")
        return result
    except Exception as e:
        logger.error(f"Error saving data to sheet: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/parse_invoice")
async def parse_invoice_rt(
    input_data: ParseInvoiceUrl, background_tasks: BackgroundTasks
):
    """
    Parse invoice data from a given URL
    """

    background_tasks.add_task(
        invoice_to_telegram_bot, input_data.url, input_data.chat_id
    )
    return {
        "message": "Чек принят в обработку. Результат будет отправлен в телеграм бот."
    }


@router.post("/invoice/{invoice_id}")
async def get_invoice_data_rt(invoice_id: str):
    """
    Get invoice data from data
    """
    try:
        invoice = await redis.get("invoice:%s" % invoice_id)
        if not invoice:
            logger.error("Invoice with id <%s> Not Found" % invoice_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice with id <%s> Not Found" % invoice_id,
            )
        return json.loads(invoice)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error get invoice data with id <%s>: %s" % (invoice_id, e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/invoice-to-sheet")
async def invoice_to_sheet_rt(data: InvoiceToSheet):
    """
    Invoice data from mini app after sorting
    """
    date = datetime.datetime.strptime(data.date, "%d/%m/%Y %H:%M")
    try:
        result = []
        for i in data.items:
            response = append_value_sheet(
                date=str(date),
                amount=i["amount"] * 0.01,
                category=i["category"],
                note="трата",
            )
            logger.info(f"Data to be saved to sheet: {data}")
            result.append(response)
        return result
    except Exception as e:
        logger.error(f"Error saving data to sheet: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
