# CardWapas (working title)

QR-based lost metro card recovery. Owner sticks a QR on their card. A finder scans it (no login),
reports the card found, and the owner is notified. See PRD.md for the full spec.

## Quick start (everyone)

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # then edit .env (set SECRET_KEY at least)
flask --app app run --debug
```

Open http://127.0.0.1:5000. With no email configured, notification emails are printed in the terminal.

To test the QR scan from a real phone on the same Wi-Fi, set `BASE_URL` in `.env` to your laptop's
LAN address (for example `http://192.168.1.5:5000`) and run `flask --app app run --host 0.0.0.0`.

## Project layout and ownership

| File / folder | Purpose | Owner |
|---|---|---|
| `app.py`, `config.py`, `extensions.py`, `models.py` | App setup, settings, database models | Person 1 |
| `routes/cards.py`, `routes/reports.py` | Dashboard, add card, QR download, reply, recover | Person 1 |
| `routes/found.py` | Public finder page and report | Person 1 + Person 2 |
| `routes/auth.py` | Register, login, logout | Person 2 |
| `templates/`, `static/` | All HTML and CSS | Person 3 |
| `services/qr.py` | QR generation | Person 4 |
| `services/notify.py` | Email to owner | Person 4 |
| `services/analytics.py` | Dashboard counters | Person 4 |

Rule: only the owner of a file edits it. If you need a change in someone else's file, message them.

## Shared interfaces (agreed contract, do not rename without telling the team)

- `generate_qr_png(url) -> BytesIO`, `build_found_url(token) -> str` in `services/qr.py`
- `send_owner_email(owner, card, report) -> bool` in `services/notify.py` (never raises)
- `get_stats(owner_id=None) -> dict` in `services/analytics.py`
- Routes: see the table in PRD.md section 12

## Task checklists

**Person 1 (Backend lead)**
- [ ] Repo on GitHub, everyone added, `main` branch protected by convention
- [ ] Confirm models cover what the team needs (latitude/longitude are there for the optional map)
- [ ] Route to regenerate a card's token and delete a card (see TODO in `routes/cards.py`)
- [ ] Deployment (Render or PythonAnywhere), set env vars there, confirm HTTPS
- [ ] Merge teammates' branches into `main` regularly

**Person 2 (Auth and security)**
- [ ] Rate limit `/login`
- [ ] Verify the 5-per-hour limit on the found page actually blocks the 6th POST
- [ ] Try to break it: guess tokens, submit `<script>` text, visit another owner's report or card IDs
- [ ] Confirm no public page ever shows owner name, email, or phone
- [ ] Optional: CAPTCHA on the found page
- [ ] Write the "Security" section of the pitch

**Person 3 (Frontend)**
- [ ] Edit `MEETUP_POINTS` in `config.py` to real spots
- [ ] Make `found.html` quick and clean on a phone
- [ ] Auto-refresh `report_status.html`
- [ ] Polish dashboard layout, empty states, and the look of the stat tiles
- [ ] Optional: Leaflet map pin (saves `latitude`/`longitude`)

**Person 4 (Integrations and demo)**
- [ ] Test email with a Gmail app password; keep console mode as the fallback
- [ ] Printable sticker sheet (QR plus "Found this card? Scan to return it")
- [ ] Print a real QR and stick it on a real card for the demo
- [ ] Pitch slides and demo script (see PRD.md section 16)

## Git workflow

- One branch per person (`p1-backend`, `p2-auth`, `p3-frontend`, `p4-integrations`).
- Commit small, pull from `main` often, merge into `main` at least every 3 hours.
- Never commit `.env` or the `.db` file (already in `.gitignore`).

## Known limitations of this skeleton

- Written against the stack in PRD.md but not yet run end to end by the author, so expect small
  fixes on first run. Do the quick start together in the first hour and fix anything that breaks.
- Forms are protected with Flask-WTF CSRF tokens. If you add a new form, include
  `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`.
