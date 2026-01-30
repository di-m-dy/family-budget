"""
Keyboards for the Telegram bot.
"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

web_app_main_button = InlineKeyboardButton(
    text="Scan QR", web_app=WebAppInfo(url="https://front.dimdy-dev.com/")
)


def web_app():
    buttons = [[web_app_main_button]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard


def web_app_invoice(iic: str):
    buttons = [
        [
            InlineKeyboardButton(
                text="Отсортировать",
                web_app=WebAppInfo(
                    url="https://front.dimdy-dev.com/?invoice=%s" % iic
                ),  # TODO: reading at react parameter
            )
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=1)
    return keyboard
