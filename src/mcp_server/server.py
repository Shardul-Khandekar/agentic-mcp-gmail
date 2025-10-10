from __future__ import annotations
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field
from fastmcp import FastMCP

from .gmail_service import send_email


class SendEmailInput(BaseModel):
    to: List[EmailStr] = Field(min_length=1, description="Primary Recipient")
    subject: str = Field(min_length=1)
    body: str = Field(min_length=1)
    cc: Optional[List[EmailStr]] = Field(default=None)
    bcc: Optional[List[EmailStr]] = Field(default=None)
    is_html: bool = Field(default=False)


mcp = FastMCP("gmail-mcp")


@mcp.tool
def gmail_send(payload: SendEmailInput):
    """
    Minimal wrapper around gmail_service.send_email.
    """
    msg_id = send_email(
        to=payload.to,
        cc=payload.cc,
        bcc=payload.bcc,
        subject=payload.subject.strip(),
        body=payload.body.strip(),
        is_html=payload.is_html,
    )
    return {"status": "sent", "id": msg_id}


if __name__ == "__main__":
    mcp.run()
