"""
fastapi-resend: Fast, modern transactional email sender for FastAPI powered by Resend.
Supports async execution, background tasks, and HTML templates.
"""

from typing import List, Optional, Union
import httpx
from fastapi import BackgroundTasks, HTTPException, status

RESEND_API_URL = "https://api.resend.com/emails"

class ResendMailer:
    """
    FastAPI mailer utility for Resend.

    Usage:
        mailer = ResendMailer(api_key="re_...", from_email="Acme <hello@acme.com>")

        await mailer.send(
            to="user@example.com",
            subject="Hello",
            html="<h1>Welcome</h1>"
        )
    """
    def __init__(self, api_key: str, from_email: str):
        self.api_key = api_key
        self.from_email = from_email

    async def send(
        self,
        to: Union[str, List[str]],
        subject: str,
        html: Optional[str] = None,
        text: Optional[str] = None,
        reply_to: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ) -> dict:
        """Send an email asynchronously via Resend API."""
        recipients = [to] if isinstance(to, str) else to

        payload = {
            "from": self.from_email,
            "to": recipients,
            "subject": subject,
        }
        if html:
            payload["html"] = html
        if text:
            payload["text"] = text
        if reply_to:
            payload["reply_to"] = reply_to
        if cc:
            payload["cc"] = cc
        if bcc:
            payload["bcc"] = bcc

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.post(RESEND_API_URL, json=payload, headers=headers)
            if res.status_code >= 400:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Resend error ({res.status_code}): {res.text}"
                )
            return res.json()

    def send_in_background(
        self,
        background_tasks: BackgroundTasks,
        to: Union[str, List[str]],
        subject: str,
        html: Optional[str] = None,
        text: Optional[str] = None
    ):
        """Schedule email to be sent in background after HTTP response is returned."""
        background_tasks.add_task(self.send, to=to, subject=subject, html=html, text=text)
