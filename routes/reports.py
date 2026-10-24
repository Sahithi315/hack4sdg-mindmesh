"""Owner actions on found reports.  OWNER: Person 1 (Backend lead)."""
from flask import Blueprint, abort, flash, redirect, url_for, request
from flask_login import current_user, login_required

from extensions import db
from models import FoundReport, utcnow

bp = Blueprint("reports", __name__)


def _owned_report_or_404(report_id):
    report = db.session.get(FoundReport, report_id)
    if report is None or report.card.owner_id != current_user.id:
        abort(404)
    return report


@bp.route("/reports/<int:report_id>/reply", methods=["POST"])
@login_required
def reply(report_id):
    report = _owned_report_or_404(report_id)
    text = request.form.get("owner_reply", "").strip()[:300]
    if text:
        report.owner_reply = text
        if report.status == "new":
            report.status = "owner_replied"
        db.session.commit()
        flash("Reply saved. The finder can see it on their status page.", "success")
    return redirect(url_for("cards.dashboard"))


@bp.route("/reports/<int:report_id>/recover", methods=["POST"])
@login_required
def recover(report_id):
    report = _owned_report_or_404(report_id)
    if report.status != "recovered":
        report.status = "recovered"
        report.recovered_at = utcnow()
        report.card.status = "active"
        db.session.commit()
        flash("Marked as recovered. Great!", "success")
    return redirect(url_for("cards.dashboard"))
