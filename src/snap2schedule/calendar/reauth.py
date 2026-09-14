"""
reauth.py - Re-authenticate with Google Calendar OAuth2.
Xóa token cũ và chạy lại OAuth flow để lấy token mới.

Usage (chạy từ thư mục gốc d:\\Snap2Schedule):
    .venv\\Scripts\\python.exe src/snap2schedule/calendar/reauth.py
"""

from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

# Paths relative to project root (d:\Snap2Schedule)
_HERE = Path(__file__).parent  # src/snap2schedule/calendar/
_CREDS_DIR = _HERE.parent / "credentials"
TOKEN_PATH = _CREDS_DIR / "token.json"
CREDS_PATH = _CREDS_DIR / "credentials.json"


def reauth() -> None:
    creds = None

    # 1. Try loading existing token
    if TOKEN_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
            print(f"[INFO] Loaded existing token from {TOKEN_PATH}")
        except Exception as e:
            print(f"[WARN] Could not load token: {e}")
            creds = None

    # 2. Try refreshing if expired but refresh_token still present
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            print("[OK] Token refreshed successfully.")
        except Exception as e:
            print(f"[WARN] Refresh failed ({e}). Will run full OAuth flow.")
            creds = None

    # 3. Full OAuth browser flow
    if not creds or not creds.valid:
        if not CREDS_PATH.exists():
            raise FileNotFoundError(
                f"credentials.json not found at {CREDS_PATH}\n"
                "Download it from Google Cloud Console → APIs & Services → Credentials."
            )

        print("[INFO] Opening browser for Google login...")
        flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_PATH), SCOPES)
        creds = flow.run_local_server(port=0)
        print("[OK] Authentication successful.")

    # 4. Save new token
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    print(f"[OK] Token saved to {TOKEN_PATH}")
    print()
    print("Bây giờ có thể chạy app bình thường:")
    print("  .venv\\Scripts\\streamlit.exe run src/snap2schedule/app.py")


if __name__ == "__main__":
    reauth()
