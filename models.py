"""Database models.  OWNER: Person 1 (Backend lead).
Agree on any change to these in the team chat first, since everyone depends on them."""
import secrets
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, login_manager


def utcnow():
    # Naive UTC datetime (SQLite stores naive datetimes).
    return datetime.now(timezone.utc).replace(tzinfo=None)


def new_token():
    # 16 random bytes -> ~22 URL-safe characters. Unguessable.
    return secrets.token_urlsafe(16)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20))  # optional, never shown to finders
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)

    cards = db.relationship("Card", backref="owner", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    label = db.Column(db.String(60), nullable=False, default="My metro card")
    token = db.Column(db.String(64), unique=True, nullable=False, index=True, default=new_token)
    status = db.Column(db.String(20), nullable=False, default="active")  # active | lost
    created_at = db.Column(db.DateTime, default=utcnow)

    reports = db.relationship(
        "FoundReport", backref="card", lazy=True, order_by="FoundReport.created_at.desc()"
    )


class FoundReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"), nullable=False)
    message = db.Column(db.Text)
    meetup_point = db.Column(db.String(120))
    meetup_note = db.Column(db.String(200))
    finder_contact = db.Column(db.String(120))  # optional, finder chooses to share
    latitude = db.Column(db.Float)   # optional, for the map stretch goal
    longitude = db.Column(db.Float)  # optional, for the map stretch goal
    report_token = db.Column(db.String(64), unique=True, nullable=False, index=True, default=new_token)
    status = db.Column(db.String(20), nullable=False, default="new")  # new | owner_replied | recovered
    owner_reply = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=utcnow)
    recovered_at = db.Column(db.DateTime)


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (ValueError, TypeError):
        return None
