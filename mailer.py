import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from config import SMTP_HOST, SMTP_PORT


def send(subject: str, html: str, images: list[tuple[str, Path]]) -> None:
    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = os.environ["MAIL_FROM"]
    msg["To"] = os.environ["MAIL_TO"]
    msg.attach(MIMEText(html, "html", "utf-8"))
    for cid, path in images:
        inline = MIMEImage(path.read_bytes())
        inline.add_header("Content-ID", f"<{cid}>")
        inline.add_header("Content-Disposition", "inline", filename=f"{cid}.png")
        msg.attach(inline)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as s:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(os.environ["MAIL_FROM"], os.environ["SMTP"])
        s.send_message(msg)
