"""App configuration. Values come from environment variables (see .env.example)."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
    _db_url = os.environ.get("DATABASE_URL", "sqlite:///cardwapas.db")
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Used to build the URL stored inside each QR code.
    BASE_URL = os.environ.get("BASE_URL", "")

    # Email settings (if MAIL_USERNAME is empty, emails are printed to the console).
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_SENDER = os.environ.get("MAIL_SENDER", "") or os.environ.get("MAIL_USERNAME", "")

    # Preset safe public meetup points shown on the finder page.
    # TODO (Person 3): edit these to real spots for your campus / metro station.
    MEETUP_POINTS = [
        "RVCE main gate",
        "Library entrance",
        "Canteen",
        "Metro station concourse (public area)",
        "Other (describe in the note)",
    ]
