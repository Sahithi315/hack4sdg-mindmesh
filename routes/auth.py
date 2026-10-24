"""Register / login / logout.  OWNER: Person 2 (Auth and security)."""
import re
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db, limiter
from models import User

bp = Blueprint("auth", __name__)

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
DUMMY_HASH = generate_password_hash("dummy-salt-for-timing-mitigation")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("cards.dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")

        if not name:
            flash("Please enter your name.", "danger")
        elif not email:
            flash("Please enter your email address.", "danger")
        elif not EMAIL_REGEX.match(email):
            flash("Please enter a valid email address.", "danger")
        elif len(password) < 8:
            flash("Password must be at least 8 characters long.", "danger")
        elif not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
            flash("Password must contain at least one letter and one number.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("That email is already registered. Try logging in.", "danger")
        else:
            user = User(name=name[:80], email=email[:120], phone=phone[:20] or None)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Account created successfully! Welcome to CardWapas.", "success")
            return redirect(url_for("cards.dashboard"))

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("cards.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if user:
            password_ok = user.check_password(password)
        else:
            # Perform dummy hash check to mitigate timing-based user enumeration
            check_password_hash(DUMMY_HASH, password)
            password_ok = False

        if password_ok:
            login_user(user)
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/") and not next_page.startswith("//") and not next_page.startswith("/\\"):
                return redirect(next_page)
            return redirect(url_for("cards.dashboard"))

        # Uniform error message so login never reveals whether an email exists
        flash("Wrong email or password.", "danger")

    return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
