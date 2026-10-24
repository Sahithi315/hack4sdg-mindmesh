# AGENTS.md - CardWapas project rules

## What this project is
CardWapas is a Flask web app for recovering lost metro cards. The owner sticks a unique QR on a card.
A finder scans it (NO login), reports the card found, and the owner is notified. Full spec: PRD.md.
It is a 24-hour hackathon project built by a team of 4 beginners, so keep everything simple and readable.

## Tech stack (do not change without asking)
- Python 3 + Flask, Flask-SQLAlchemy (SQLite), Flask-Login, Flask-Limiter, Flask-WTF (CSRF)
- Jinja2 templates + Bootstrap 5 (CDN). No React, no build step, no npm.
- `qrcode[pil]` for QR images. Email via smtplib (console fallback when MAIL_USERNAME is empty).

## Run
`flask --app app run --debug`  (see README.md for full setup)

## File ownership (important)
Each teammate owns specific files. Only edit files belonging to the person you are working for.
If a change is needed in someone else's file, STOP and tell the user instead of editing it.
- Person 1 (Backend): app.py, config.py, extensions.py, models.py, routes/cards.py, routes/reports.py, routes/found.py
- Person 2 (Auth and security): routes/auth.py (and security review of routes/found.py)
- Person 3 (Frontend): templates/*, static/*
- Person 4 (Integrations and demo): services/qr.py, services/notify.py, services/analytics.py

## Shared interfaces (never rename or change signatures)
- `generate_qr_png(url) -> BytesIO` and `build_found_url(token) -> str` in services/qr.py
- `send_owner_email(owner, card, report) -> bool` in services/notify.py (must never raise)
- `get_stats(owner_id=None) -> dict` in services/analytics.py
- Route names/endpoints listed in PRD.md section 12

## Privacy and security rules (non-negotiable)
- Public pages (/found/<token>, /report/<report_token>) must NEVER show the owner's name, email, or phone.
- The QR contains only a public URL with a random token. Never put a login session or personal data in it.
- Never log or commit secrets. `.env` and `*.db` must stay out of git.
- Every POST form needs `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`.
- Never use `|safe` on user-supplied text. Validate and length-limit all user input.
- Owner-only routes must check ownership (a user must not access another user's cards or reports).

## Code style
- Beginner-friendly: small functions, clear names, a short comment explaining WHY when non-obvious.
- Follow PEP 8. Do not add new libraries unless asked; if one is truly needed, say so and add it to requirements.txt.
- Do not rewrite working code unnecessarily. Make the smallest change that does the job.

## Working agreement
- Work on your own git branch. Do not push to main directly.
- After each task, summarize what you changed and give the exact steps to test it manually in the browser.
- If something in these instructions or PRD.md conflicts with a request, ask before proceeding.
