from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/calendar.events"
]


def get_calendar_service():
    token_path = Path("src/snap2schedule/credentials/token.json")

    if not token_path.exists():
        raise FileNotFoundError(
            "token.json not found. Run OAuth flow first."
        )

    creds = Credentials.from_authorized_user_file(
        token_path,
        SCOPES,
    )

    service = build(
        "calendar",
        "v3",
        credentials=creds,
    )

    return service