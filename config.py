"""App configuration. Values come from environment variables (see .env.example)."""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Database -------------------------------------------------------------
# Locally this is SQLite. On Render, set DATABASE_URL to the Postgres "Internal Database URL".
_db_url = os.environ.get("DATABASE_URL", "sqlite:///cardwapas.db")
# Some providers give "postgres://", but SQLAlchemy needs "postgresql://".
if _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql://", 1)

# --- Environment ------------------------------------------------------------
_base_url = os.environ.get("BASE_URL", "").rstrip("/")
_secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

# Treat the app as "production" when it runs on an https address or on Render
# (Render sets the RENDER environment variable automatically).
_is_production = _base_url.startswith("https") or bool(os.environ.get("RENDER"))

if _is_production and _secret_key == "dev-only-change-me":
    raise RuntimeError(
        "SECRET_KEY is not set. In production you must set a long random SECRET_KEY "
        "environment variable. Generate one with: "
        'python -c "import secrets; print(secrets.token_hex(32))"'
    )


class Config:
    SECRET_KEY = _secret_key
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Checks a database connection is alive before using it (avoids errors after idle time).
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # Used to build the URL stored inside each QR code (no trailing slash).
    BASE_URL = _base_url

    # Cookie safety. SECURE only when the site is served over https, so local http still works.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = _base_url.startswith("https")

    # SMTP email settings. NOTE: Render's free tier blocks SMTP ports, so on Render leave
    # MAIL_USERNAME empty (emails are printed to the logs) or use the Brevo API (BREVO_* variables,
    # read directly by services/notify.py).
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