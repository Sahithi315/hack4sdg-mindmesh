"""Email notifications.  OWNER: Person 4 (Integrations and demo).

If MAIL_USERNAME is not set, the email is printed to the console instead,
so the rest of the flow can be developed and tested without email working.
"""
import smtplib
from email.message import EmailMessage

from flask import current_app


def send_owner_email(owner, card, report):
    """Tell the owner that someone found their card.

    Privacy rule: do NOT include finder contact details in the email.
    The owner reads the full report on the dashboard after logging in.

    Returns True if sent (or printed), False if sending failed.
    This must never raise, because a mail failure should not break the finder's submission.
    """
    cfg = current_app.config
    base = cfg.get("BASE_URL", "").rstrip("/")
    subject = f"Someone found your card: {card.label}"
    body = (
        f"Hi {owner.name},\n\n"
        f"Good news! Someone scanned the QR on your card \"{card.label}\" and reported it found.\n\n"
        f"Suggested meetup: {report.meetup_point or 'not specified'}\n\n"
        f"Log in to see the details and reply: {base}/dashboard\n\n"
        f"- CardWapas"
    )

    if not cfg.get("MAIL_USERNAME"):
        print("\n=== EMAIL (console mode) ===")
        print(f"To: {owner.email}\nSubject: {subject}\n\n{body}")
        print("=== END EMAIL ===\n")
        return True

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = cfg["MAIL_SENDER"]
        msg["To"] = owner.email
        msg.set_content(body)
        with smtplib.SMTP(cfg["MAIL_SERVER"], cfg["MAIL_PORT"], timeout=10) as server:
            server.starttls()
            server.login(cfg["MAIL_USERNAME"], cfg["MAIL_PASSWORD"])
            server.send_message(msg)
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"[notify] email failed: {exc}")
        return False
