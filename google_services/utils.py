"""
Utils for Google services.
"""

import datetime
import logging

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_services.cred import get_token

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]


def get_calendar_events(calendar_id: str = "primary"):
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
                calendarId=calendar_id,
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
        logger.error(f"An error occurred: {error}")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_values_sheet(spreadsheet_id, range_name):
    """
    Get values from Google Sheet
    """
    creds = get_token(SCOPES)
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
        logger.error(f"An http error occurred: {error}")
        raise error
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e


def append_value_sheet(
    date: str,
    amount: str,
    category: str,
    note: str,
    spreadsheet_id: str,
    range_name: str,
):
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
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body={"values": [[date, amount, note, category]]},
            )
            .execute()
        )
        return result
    except HttpError as error:
        logger.error(f"An error occurred: {error}")
        raise error
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e
