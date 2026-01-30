"""
Module for handlers message and commands.
"""

import logging

from aiogram import F, Router, types

from bot.keyboards import web_app

logger = logging.getLogger(__name__)

router = Router()


@router.message(F.text == "/start")
async def start_cmd_handler(message: types.Message):
    """
    Handler for the /start command.
    """
    await message.answer("Привет! Давай беречь бюджет!")


@router.message(F.text == "/webapp")
async def test_web_app(message: types.Message):
    """
    Test web app button
    """
    await message.answer(
        text="Просканируй QR код, нажав на кнопку ниже", reply_markup=web_app()
    )
