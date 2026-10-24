# Antigravity prompts for each teammate

## How to use
1. Everyone clones the GitHub repo and opens the folder in Antigravity as a workspace.
2. Antigravity reads AGENTS.md automatically. Keep PRD.md in the repo root so the agent can read it.
3. Create your own branch first (see the Git step in each prompt).
4. Use **Planning** mode for the bigger prompts, **Fast** mode for small fixes.
5. Paste ONE prompt at a time, review what the agent plans, then approve. Test in the browser before the next prompt.

---

## Step 0 - Person 1 only, FIRST (everyone else waits for this to be merged)

```
Read AGENTS.md, README.md and PRD.md. You are working as Person 1 (Backend lead).

The project skeleton has never been run end to end. Goal: make the app run cleanly.
1. Create a virtual environment, install requirements.txt, copy .env.example to .env.
2. Start the app with `flask --app app run --debug` and fix any import errors, typos, or crashes.
3. Manually walk through the full flow: register -> log in -> add a card -> view the QR ->
   open /found/<token> in a private window -> submit a report -> reply and mark recovered on the dashboard.
4. Fix every bug you find, editing only the files Person 1 owns. If a bug is in someone else's file,
   list it for me instead of editing.
5. Do not add new features.

When done, give me a list of what you fixed and confirm each step of the flow works.
```
Then commit and push to `main` so the other three start from a working base.

---

## Person 1 - Backend lead

```
Read AGENTS.md and PRD.md. You are Person 1 (Backend lead). Edit only: app.py, config.py,
extensions.py, models.py, routes/cards.py, routes/reports.py, routes/found.py.

Tasks:
1. In routes/cards.py add: (a) POST /cards/<id>/regenerate-token that creates a new random token for an
   owned card (old QR stops working), and (b) POST /cards/<id>/delete that deletes an owned card and its reports.
   Both must check ownership and use CSRF.
2. Add a minimal /healthz route in app.py that returns "ok" (useful for deployment).
3. Prepare for deployment on Render: confirm the Procfile works with gunicorn "app:create_app()",
   and list the environment variables I must set (SECRET_KEY, BASE_URL, MAIL_*, DATABASE_URL).
4. Do not change function signatures listed under "Shared interfaces" in AGENTS.md.

Tell Person 3 (in your summary) which template variables each route passes, so they can add buttons for
regenerate and delete. Give manual test steps for each new route.
```

---

## Person 2 - Auth and security

```
Read AGENTS.md and PRD.md. You are Person 2 (Auth and security). Edit only routes/auth.py.
You may REVIEW routes/found.py, routes/cards.py and routes/reports.py but must not edit them;
report problems to me instead.

Tasks:
1. Add rate limiting to POST /login (10 per minute per IP) using the existing `limiter`.
2. Strengthen registration: require a valid-looking email, password length >= 8 and at least one
   letter and one number, and give clear flash messages.
3. Make sure login does not reveal whether an email exists (same error message for wrong email or password).
4. Security review. Check and report on: (a) any page that could leak owner name/email/phone to a finder,
   (b) any owner route that does not verify ownership, (c) any place user input is rendered unescaped,
   (d) any form missing a CSRF token, (e) whether the 5-per-hour limit on /found/<token> really blocks the 6th POST.
5. Write a short list of the 5 most important security measures in this project, in plain English,
   for our pitch slides.

Give me the review as a table: issue, file, severity, suggested fix.
```

---

## Person 3 - Frontend

```
Read AGENTS.md and PRD.md. You are Person 3 (Frontend). Edit only files in templates/ and static/.
Do not edit any .py file.

Tasks:
1. Make templates/found.html fast and clean on a phone (large tap targets, minimal scrolling),
   since finders will be standing somewhere holding a card. Keep the privacy rule: never show owner details.
2. Add auto-refresh to templates/report_status.html (reload every 30 seconds with a small
   `<meta http-equiv="refresh">` or a few lines of JavaScript) so the finder sees the owner's reply.
3. Improve templates/dashboard.html: clearer sections, empty states, status badges, and a friendlier
   look for the four stat tiles. Keep every form's csrf_token field and every existing field name.
4. Add a simple landing page section on the login page explaining the idea in 2-3 lines
   ("Stick a QR on your metro card. If someone finds it, they can reach you without seeing your number.").
5. Keep it Bootstrap only. No new JavaScript frameworks.

Show me screenshots or a description of each page on a phone-sized screen, and list any route or variable
you need from the backend that does not exist yet (do not add it yourself).
```

---

## Person 4 - Integrations and demo

```
Read AGENTS.md and PRD.md. You are Person 4 (Integrations and demo). Edit only services/qr.py,
services/notify.py and services/analytics.py. You may also create new files under a new folder
`demo/` for slides and scripts.

Tasks:
1. services/qr.py: add `generate_sticker_png(url, label)` that returns a BytesIO PNG of a small
   printable sticker: the QR code plus the text "Found this card? Scan to return it to its owner"
   and the card label, using Pillow. Keep `generate_qr_png` unchanged.
2. services/notify.py: make email sending robust (short timeout, never raises, console fallback stays).
   Make the email text friendly and short. Do not include finder contact details in the email.
3. Explain, step by step for a beginner, how to create a Gmail App Password and set MAIL_USERNAME,
   MAIL_PASSWORD and MAIL_SENDER in .env, and how to test it.
4. services/analytics.py: confirm get_stats works with zero data (no division by zero) and with
   recovered reports.
5. Create demo/DEMO_SCRIPT.md: a 3-minute live demo script (problem, register, add card, scan,
   report, owner notified, recovered, SDG 12 close) with who does what among 4 people.
6. Create demo/PITCH_OUTLINE.md: 6-slide outline (problem, idea, how it works, tech, SDG impact, future scope).

List what Person 1 or Person 3 must change to use the new sticker function (do not edit their files).
```

---

## Final integration - Person 1, around hour 19

```
Read AGENTS.md, README.md and PRD.md. Merge status check:
1. Walk through the whole flow again and list anything broken.
2. Confirm: no public page shows owner details, .env and *.db are not tracked by git,
   requirements.txt includes every library used.
3. Give me a deployment checklist for Render with the exact settings to enter.
Only fix issues in files Person 1 owns; list the rest by owner.
```
