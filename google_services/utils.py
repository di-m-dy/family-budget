"""
Utils for Google services.
"""

import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_services.cred import get_token

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]

SPREADSHEET_ID = "1q8s35_JqYKJQFtxRCE_Elo1vl8BNGJ9qQk4GMQAdAvU"
RANGE_NAME = "2025!A5:D"


def get_calendar_events():
    """
    Get events from calendar
    """

    creds = get_token(SCOPES)

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        return events

    except HttpError as error:
        print(f"An error occurred: {error}")


def get_values_sheet(spreadsheet_id, range_name):
    """
    Get values from Google Sheet
    """
    creds = get_token(SCOPES)
    # pylint: disable=maybe-no-member
    try:
        service = build("sheets", "v4", credentials=creds)

        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=range_name)
            .execute()
        )
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


def append_value_sheet(date: str, amount: str, category: str, note: str):
    """
    Append value to Google Sheet
    """
    creds = get_token(SCOPES)
    # pylint: disable=maybe-no-member
    try:
        service = build("sheets", "v4", credentials=creds)

        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption="USER_ENTERED",
                body={"values": [[date, amount, note, category]]},
            )
            .execute()
        )
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
