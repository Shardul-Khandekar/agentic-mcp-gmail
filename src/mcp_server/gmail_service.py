import base64
import os
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable, List, Optional

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()
SCOPES = (os.getenv("GOOGLE_OAUTH_SCOPES")
          or "https://www.googleapis.com/auth/gmail.send").split()
TOKEN_PATH = Path(os.getenv("GMAIL_TOKEN_PATH")
                  or "~/.mcp/gmail.json").expanduser()


# Convert to, from, cc, bcc to list
def as_list(value: Optional[Iterable[str]]) -> List[str]:
    # If value is None or empty, return empty list
    if not value:
        return []
    # If value is a string, split by comma and strip whitespace
    if isinstance(value, (str,)):
        return [p.strip() for p in value.split(",") if p.strip()]
    else:
        # If value is already an iterable, convert each item to string and strip whitespace
        return [str(x).strip() for x in value if str(x).strip()]


def gmail_service():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    return build("gmail", "v1", credentials=creds)


# The * in the function signature forces the use of keyword arguments when calling the function
def send_email(*, to: Iterable[str], subject: str, body: str,
               cc: Optional[Iterable[str]] = None,
               bcc: Optional[Iterable[str]] = None,
               is_html: bool = False) -> str:

    # Convert the to list
    to_list = as_list(to)
    if not to_list:
        raise ValueError("At least one recipient is required (to).")

    cc_list = as_list(cc)
    bcc_list = as_list(bcc)

    # Create the email message
    msg = EmailMessage()

    # To, Cc, Bcc and Subject headers
    msg["To"] = ", ".join(to_list)
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)
    if bcc_list:
        msg["Bcc"] = ", ".join(bcc_list)
    msg["Subject"] = subject.strip()

    # Set the email body, it can either be plain text or HTML
    subtype = "html" if is_html else "plain"
    msg.set_content(body.strip(), subtype=subtype)

    # Encode the message in base64 format
    # Gmail API requires the message to be base64url encoded string inside "raw" field of request body
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    service = gmail_service()

    # UserId "me" indicates the currently authenticated user by the OAuth token.
    res = service.users().messages().send(
        userId="me", body={"raw": raw}).execute()
    return res.get("id", "")
