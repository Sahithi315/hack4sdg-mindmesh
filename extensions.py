"""Shared Flask extension objects. Created here, attached to the app in app.py.
Keeping them in one file avoids circular imports."""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to continue."

limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")
