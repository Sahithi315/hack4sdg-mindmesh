"""Impact numbers for the dashboard.  OWNER: Person 4 (Integrations and demo)."""
from models import Card, FoundReport


def get_stats(owner_id=None):
    """Counters for the dashboard. Pass owner_id for one user, or None for the whole system
    (handy for the pitch: "X cards registered, Y recovered")."""
    cards_q = Card.query
    if owner_id is not None:
        cards_q = cards_q.filter_by(owner_id=owner_id)
    cards = cards_q.all()
    card_ids = [c.id for c in cards]

    reports = []
    if card_ids:
        reports = FoundReport.query.filter(FoundReport.card_id.in_(card_ids)).all()

    recovered = [r for r in reports if r.status == "recovered" and r.recovered_at]
    avg_hours = None
    if recovered:
        total_seconds = sum((r.recovered_at - r.created_at).total_seconds() for r in recovered)
        avg_hours = round(total_seconds / len(recovered) / 3600, 1)

    return {
        "cards": len(cards),
        "reports": len(reports),
        "recovered": len(recovered),
        "avg_hours_to_recover": avg_hours,
    }
