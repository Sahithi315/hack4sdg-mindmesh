"""Email notifications.  OWNER: Person 4 (Integrations and demo).

If MAIL_USERNAME is not set, the email is printed to the console instead,
so the rest of the flow can be developed and tested without email working.
"""
import smtplib
from email.message import EmailMessage

from flask import current_app, request


def send_owner_email(owner, card, report):
    """Tell the owner that someone found their card.

    Privacy rule: do NOT include finder contact details in the email.
    The owner reads the full report on the dashboard after logging in.

    Returns True if sent (or printed in console mode), False if sending failed.
    This must never raise, because a mail failure should not break the finder's submission.
    """
    try:
        if not owner or not getattr(owner, "email", None):
            print("[notify] email skipped: owner or owner.email is missing")
            return False

        cfg = current_app.config
        base = (cfg.get("BASE_URL") or "").rstrip("/")
        if not base:
            try:
                base = request.url_root.rstrip("/")
            except Exception:
                base = "http://127.0.0.1:5000"

        dashboard_url = f"{base}/dashboard"
        owner_name = getattr(owner, "name", "there") or "there"
        card_label = getattr(card, "label", "metro card") or "metro card"
        meetup = getattr(report, "meetup_point", None) or "Not specified"

        subject = f"Good news! Someone found your card: {card_label}"
        body = (
            f"Hi {owner_name},\n\n"
            f"Good news! Someone found your card \"{card_label}\" and reported it on CardWapas.\n\n"
            f"Suggested meetup: {meetup}\n\n"
            f"Log in to your dashboard to review the report and coordinate the return:\n"
            f"{dashboard_url}\n\n"
            f"- Team CardWapas"
        )

        mail_username = (cfg.get("MAIL_USERNAME") or "").strip()
        if not mail_username:
            print("\n=== EMAIL (console mode) ===")
            print(f"To: {owner.email}\nSubject: {subject}\n\n{body}")
            print("=== END EMAIL ===\n")
            return True

        sender = (cfg.get("MAIL_SENDER") or mail_username).strip()
        password = cfg.get("MAIL_PASSWORD", "")
        server_host = cfg.get("MAIL_SERVER", "smtp.gmail.com")
        try:
            server_port = int(cfg.get("MAIL_PORT", 587))
        except (TypeError, ValueError):
            server_port = 587

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = owner.email
        msg.set_content(body)

        # Short timeout (5s) so network/SMTP stalls never freeze the user's browser
        timeout_seconds = 5
        if server_port == 465:
            with smtplib.SMTP_SSL(server_host, server_port, timeout=timeout_seconds) as server:
                server.login(mail_username, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(server_host, server_port, timeout=timeout_seconds) as server:
                server.starttls()
                server.login(mail_username, password)
                server.send_message(msg)

        return True
    except Exception as exc:  # noqa: BLE001
        print(f"[notify] email failed: {exc}")
        return False
