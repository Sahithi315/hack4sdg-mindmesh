"""Public pages for the finder (NO login).  OWNER: Person 1 (Backend) + Person 2 (security).

Security notes (Person 2 please double-check):
  - Never show owner name/email/phone on these pages.
  - The POST is rate limited. Add CAPTCHA if there is time.
  - Jinja auto-escapes finder text, so keep it out of |safe.
"""
from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for

from extensions import db, limiter
from models import Card, FoundReport
from services.notify import send_owner_email

bp = Blueprint("found", __name__)


@bp.route("/found/<token>", methods=["GET", "POST"])
@limiter.limit("5 per hour", methods=["POST"])
def found(token):
    card = Card.query.filter_by(token=token).first_or_404()
    meetup_points = current_app.config["MEETUP_POINTS"]

    if request.method == "POST":
        message = request.form.get("message", "").strip()[:500]
        meetup_point = request.form.get("meetup_point", "").strip()
        meetup_note = request.form.get("meetup_note", "").strip()[:200]
        finder_contact = request.form.get("finder_contact", "").strip()[:120]
        lat = request.form.get("latitude")
        lng = request.form.get("longitude")
        try:
            latitude = float(lat) if lat else None
            longitude = float(lng) if lng else None
        except (ValueError, TypeError):
            latitude = None
            longitude = None

        if meetup_point not in meetup_points:
            flash("Please choose a meetup point.", "danger")
        else:
            report = FoundReport(
                card_id=card.id,
                message=message or None,
                meetup_point=meetup_point,
                meetup_note=meetup_note or None,
                finder_contact=finder_contact or None,
                latitude=latitude,
                longitude=longitude,
            )
            db.session.add(report)
            db.session.commit()

            send_owner_email(card.owner, card, report)  # never raises
            return redirect(url_for("found.report_status", report_token=report.report_token))

    return render_template("found.html", card=card, meetup_points=meetup_points)


@bp.route("/report/<report_token>")
def report_status(report_token):
    """Private status page for the finder (reached through an unguessable link)."""
    report = FoundReport.query.filter_by(report_token=report_token).first()
    if report is None:
        abort(404)
    return render_template("report_status.html", report=report)
