"""Register / login / logout.  OWNER: Person 2 (Auth and security).

TODO (Person 2):
  - Add rate limiting on /login (e.g. @limiter.limit("10 per minute", methods=["POST"]))
  - Enforce a stronger password rule if you have time
  - Test for open redirects, duplicate emails, and weird input
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from extensions import db
from models import User

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("cards.dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")

        if not name or not email or len(password) < 8:
            flash("Please fill in name, email, and a password of at least 8 characters.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("That email is already registered. Try logging in.", "danger")
        else:
            user = User(name=name[:80], email=email[:120], phone=phone[:20] or None)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("cards.dashboard"))

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("cards.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("cards.dashboard"))
        flash("Wrong email or password.", "danger")

    return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
