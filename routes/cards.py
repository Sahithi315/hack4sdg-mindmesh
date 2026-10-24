"""Owner dashboard and card management.  OWNER: Person 1 (Backend lead)."""
from flask import Blueprint, abort, flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required

from extensions import db
from models import Card, FoundReport, new_token
from services.analytics import get_stats
from services.qr import build_found_url, generate_qr_png

bp = Blueprint("cards", __name__)


def _owned_card_or_404(card_id):
    card = db.session.get(Card, card_id)
    if card is None or card.owner_id != current_user.id:
        abort(404)
    return card


@bp.route("/dashboard")
@login_required
def dashboard():
    cards = (
        Card.query.filter_by(owner_id=current_user.id).order_by(Card.created_at.desc()).all()
    )
    card_ids = [c.id for c in cards]
    reports = []
    if card_ids:
        reports = (
            FoundReport.query.filter(FoundReport.card_id.in_(card_ids))
            .order_by(FoundReport.created_at.desc())
            .all()
        )
    stats = get_stats(current_user.id)
    return render_template("dashboard.html", cards=cards, reports=reports, stats=stats)


@bp.route("/cards/add", methods=["POST"])
@login_required
def add_card():
    label = request.form.get("label", "").strip()[:60] or "My metro card"
    db.session.add(Card(owner_id=current_user.id, label=label))
    db.session.commit()
    flash("Card added. Download the QR and stick it on your card.", "success")
    return redirect(url_for("cards.dashboard"))


@bp.route("/cards/<int:card_id>/qr.png")
@login_required
def card_qr(card_id):
    card = _owned_card_or_404(card_id)
    buf = generate_qr_png(build_found_url(card.token))
    as_download = request.args.get("download") == "1"
    return send_file(
        buf,
        mimetype="image/png",
        as_attachment=as_download,
        download_name=f"cardwapas-qr-{card.id}.png",
    )


@bp.route("/cards/<int:card_id>/status", methods=["POST"])
@login_required
def set_card_status(card_id):
    card = _owned_card_or_404(card_id)
    new_status = request.form.get("status")
    if new_status in ("active", "lost", "recovered"):
        card.status = new_status
        db.session.commit()
    return redirect(url_for("cards.dashboard"))


@bp.route("/cards/<int:card_id>/regenerate-token", methods=["POST"])
@login_required
def regenerate_card_token(card_id):
    card = _owned_card_or_404(card_id)
    card.token = new_token()
    db.session.commit()
    flash("QR token regenerated. The old QR code will no longer work.", "success")
    return redirect(url_for("cards.dashboard"))


@bp.route("/cards/<int:card_id>/delete", methods=["POST"])
@login_required
def delete_card(card_id):
    card = _owned_card_or_404(card_id)
    label = card.label
    FoundReport.query.filter_by(card_id=card.id).delete()
    db.session.delete(card)
    db.session.commit()
    flash(f"Card \"{label}\" deleted.", "info")
    return redirect(url_for("cards.dashboard"))
