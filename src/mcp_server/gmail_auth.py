import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
SCOPES = (os.getenv("GOOGLE_OAUTH_SCOPES")
          or "https://www.googleapis.com/auth/gmail.send").split()
TOKEN_PATH = Path(os.getenv("GMAIL_TOKEN_PATH")
                  or "~/.mcp/gmail.json").expanduser()


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise SystemExit(
            "GOOGLE_OAUTH_CLIENT_ID/GOOGLE_OAUTH_CLIENT_SECRET missing in .env")

    # Build in memory client config
    client_config = {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [
                # loopback (auto-chosen by Google helper)
                "http://localhost",
                "http://127.0.0.1"            # fallback
            ]
        }
    }

    print(f"Starting Desktop OAuth flow for scopes: {SCOPES}")

    print(f"Starting Desktop OAuth flow for scopes: {SCOPES}")
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_local_server(
        host="127.0.0.1", port=0, authorization_prompt_message="",
        success_message="Authorization complete. You can close this tab.",
        open_browser=True
    )

    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_PATH, "w", encoding="utf-8") as f:
        f.write(creds.to_json())
    os.chmod(TOKEN_PATH, 0o600)

    loaded = Credentials.from_authorized_user_file(
        str(TOKEN_PATH), scopes=SCOPES)
    email_scope = "gmail.send" if "gmail.send" in " ".join(SCOPES) else SCOPES
    print(
        f"Saved token to {TOKEN_PATH} (scopes: {email_scope}); refresh_token present: {bool(loaded.refresh_token)}")


if __name__ == "__main__":
    main()
