"""Impact numbers for the dashboard.  OWNER: Person 4 (Integrations and demo)."""
from models import Card, FoundReport


def get_stats(owner_id=None):
    """Counters for the dashboard. Pass owner_id for one user, or None for the whole system
    (handy for the pitch: "X cards registered, Y recovered").

    Safe against zero data (no division by zero). When there are no recovered reports,
    avg_hours_to_recover returns None so the template can render '-' or an empty state.
    """
    cards_q = Card.query
    if owner_id is not None:
        cards_q = cards_q.filter_by(owner_id=owner_id)
    cards = cards_q.all()
    card_ids = [c.id for c in cards]

    reports = []
    if card_ids:
        reports = FoundReport.query.filter(FoundReport.card_id.in_(card_ids)).all()

    # Only include reports that reached "recovered" status and recorded a recovered_at timestamp
    recovered = [r for r in reports if r.status == "recovered" and r.recovered_at]
    avg_hours = None
    if recovered:
        # Guard against clock jitter with max(0.0, ...)
        total_seconds = sum(
            max(0.0, (r.recovered_at - r.created_at).total_seconds()) for r in recovered
        )
        avg_hours = round(total_seconds / len(recovered) / 3600, 1)

    return {
        "cards": len(cards),
        "reports": len(reports),
        "recovered": len(recovered),
        "avg_hours_to_recover": avg_hours,
    }
