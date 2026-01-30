"""
Module for schemas used in the API.
"""

from typing import List
from typing import Literal
from pydantic import BaseModel


class SendMessageRequest(BaseModel):
    """
    Schema for send message request
    """

    chat_id: int
    text: str

DataToSheetType = Literal["трата", "доход"]

class DataToSheet(BaseModel):
    """
    Schema for data to be appended to Google Sheet
    """

    date: str
    type: DataToSheetType
    amount: str
    category: str


class ParseInvoiceUrl(BaseModel):
    """
    Schema for parsed invoice data
    """

    url: str
    chat_id: int


class ParsedInvoiceData(BaseModel):
    """
    Schema for parsed invoice data response
    """

    amount: str | None = None
    place: str | None = None
    address: str | None = None
    date: str | None = None
    items: list[dict[str, str]] | None = None


class InvoiceToSheet(BaseModel):
    """
    Data from invoice to sheet
    """
    date: str
    items: List[dict] = []
