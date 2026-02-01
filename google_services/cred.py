"""
Module for managing Google API tokens.
"""

import os.path

from google.auth.exceptions import OAuthError
from google.oauth2 import service_account


def get_token(scopes):
    """
    Get API token
    """
    if not os.path.exists("service-account.json"):
        raise OAuthError()
    creds = service_account.Credentials.from_service_account_file(
        "service-account.json", scopes=scopes
    )
    return creds
