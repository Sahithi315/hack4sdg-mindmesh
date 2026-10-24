# CardWapas

**QR-Based Lost Metro Card Recovery System**

CardWapas is a web application that helps people recover lost prepaid metro cards using unique QR codes. Instead of losing the remaining balance or relying on slow metro lost-and-found processes, owners can receive recovery reports and coordinate a safe meetup with the finder.

Built for a 24-hour hackathon.

**Primary SDG:** SDG 9 — Industry, Innovation and Infrastructure (Target 9.c)
**Secondary SDG:** SDG 12 — Responsible Consumption and Production (Target 12.5)

## Live Demo

**Live app:** https://hack4sdg-mindmeshh-1.onrender.com/login

> The app runs on a free Render instance, which goes to sleep when idle. The first page load can take up to a minute, so open the link a few minutes before a demo.

---

## Problem Statement

Prepaid metro cards are anonymous. When someone loses a card, the remaining balance is often lost with it, and there is no direct way for the finder to contact its owner.

The main challenges are:

- Lost metro cards cannot easily be traced, blocked, or returned.
- Writing personal contact information on a card creates privacy risks and cannot be updated or revoked.
- Metro lost-and-found processes can be slow, manual, and unreliable.
- Replacing lost cards contributes to plastic waste.

CardWapas aims to make card recovery simple, secure, and convenient.

## Solution

CardWapas connects metro card owners with people who find their lost cards through a unique QR code.

1. The owner registers and adds their metro card.
2. CardWapas generates a unique QR code that can be downloaded and printed.
3. The owner attaches the QR code to their metro card.
4. Anyone who finds the card scans the QR code without installing an app or creating an account.
5. The finder submits a short message and selects a safe public meetup point.
6. The owner receives an email notification and reviews the report.
7. Both parties coordinate a safe handoff, and the owner marks the card as recovered.

**Goal:** Make returning a lost metro card as easy as scanning a QR code.

---

## Sustainable Development Goals

### SDG 9: Industry, Innovation and Infrastructure

CardWapas supports SDG 9, particularly target 9.c, by using accessible digital technology to solve an everyday transportation problem.

### SDG 12: Responsible Consumption and Production

CardWapas supports SDG 12, particularly target 12.5, by encouraging the recovery and reuse of existing metro cards. Recovering a lost card can help avoid unnecessary replacement cards and reduce plastic waste.

---

## Features

### Owner Features

- Secure registration and login.
- Add metro cards with custom labels.
- Generate unique QR codes for cards.
- Download QR codes as PNG images.
- View registered cards and their status.
- Mark cards as lost or active.
- Receive email notifications when a card is found.
- View finder messages and meetup details.
- Confirm or suggest another meetup point.
- Mark recovered cards as recovered.

### Finder Features

- Scan a QR code to open the recovery page.
- No login or app installation required.
- Submit a short message.
- Select a preset public meetup point.
- Add an optional meetup note.
- Optionally share contact information or location.
- Receive a private link to check the report status.

### Dashboard

The owner dashboard displays:

- Registered cards.
- Found reports.
- Recovery status.
- Recovered cards.
- Recovery analytics, including the average hours to recover.

---

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python 3 |
| Web Framework | Flask |
| Database | SQLite (local development), PostgreSQL (production) |
| ORM | Flask-SQLAlchemy |
| Authentication | Flask-Login |
| Password Security | Werkzeug password hashing |
| Frontend | HTML, CSS, Bootstrap 5 |
| Templates | Jinja2 |
| QR Code Generation | qrcode, Pillow |
| Email Notifications | SMTP (Gmail), with a console fallback |
| Rate Limiting | Flask-Limiter |
| Production Server | Gunicorn |
| Deployment | Render |
| Version Control | Git, GitHub |

---

## System Architecture

```
        Metro Card Owner
              |
       Register / Login
              |
       Add Metro Card
              |
       Generate QR Code
              |
       Print & Attach QR
              |
              v
       Finder Scans QR
              |
       Public Found Page
       (No Login Required)
              |
       Submit Found Report
              |
              v
        Flask Backend
              |
          Database
              |
        +-----+------+
        |            |
        v            v
   Owner Dashboard   Email
        |            |
        +-----+------+
              |
       Review Report
              |
       Confirm Meetup
              |
       Card Recovered
```

---

## How to Use CardWapas

### For Metro Card Owners

1. Create an account and log in.
2. Add your metro card with an optional label.
3. Download the generated QR code.
4. Print the QR code and attach it to your metro card.
5. Receive an email when someone reports your card found.
6. Open the dashboard and review the report.
7. Confirm or suggest a meetup point.
8. Meet the finder at a safe public location.
9. Mark the card as recovered.

### For Finders

1. Scan the QR code attached to the metro card.
2. Open the public recovery page.
3. Select a preset public meetup point.
4. Add a short message or meetup note.
5. Submit the found report.
6. Save the private report link to check the owner's response.
7. Coordinate the handoff through the recovery process.

---

## Demo Steps

Follow these steps to try the full recovery flow on the live app: https://hack4sdg-mindmeshh-1.onrender.com/login

**What you need:** a laptop for the owner and a phone (or a second browser window) for the finder.

### Before You Start

- Open the live link a few minutes early so the free instance is awake.
- Use the laptop for the owner and the phone for the finder.

### Step-by-Step

1. **Register the owner.** On the laptop, open the live link, register a new account, and log in.
2. **Add a card.** On the dashboard, enter a label such as "Blue metro card" and click **Generate QR**.
3. **Show the QR code.** Display it on the laptop screen or download and print it as a sticker.
4. **Scan as the finder.** On the phone, scan the QR code. The public recovery page opens with no login or app needed.
5. **Submit a found report.** Choose a preset public meetup point such as the main gate or the canteen, add an optional message, and submit.
6. **Save the finder's private link.** Keep the finder's "Thank you" page open on the phone. It shows the status "Waiting for the owner".
7. **Show the owner notification.** The owner is notified by email. If email sending is not configured, the email text appears in the server logs instead (see Email Notifications below).
8. **Review the report as the owner.** Refresh the laptop dashboard. The report appears under **Found reports** with the meetup point and the finder's message.
9. **Reply to the finder.** Type a short reply, for example "I can meet you at the main gate at 4 PM", and click **Send reply**.
10. **Show the reply on the finder's page.** Refresh the finder's page on the phone. The owner's reply appears there.
11. **Mark the card as recovered.** On the laptop, click **Mark as recovered**.
12. **Show the updated stats.** The dashboard now shows the recovered count and the average hours to recover.
13. **Close with the impact.** Every recovered card avoids a replacement card and plastic waste (SDG 12).

For a timed 3-minute version with roles for each team member, see `demo/DEMO_SCRIPT.md`.

### Demo Tips

- Add a **new** card on the live site before the demo. QR codes made on a local copy of the app point to a different address and will not work on the live site.
- Keep the finder's page open on the phone during the demo, because the owner's reply and the recovered status show up there when it is refreshed.
- Keep a backup plan ready. If the live site is slow or the network fails, run the app locally (see below) and demo from the laptop.

---

## Run Locally

1. Clone the repository and go to the folder that contains `app.py`.
2. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create your environment file from the example:

   ```
   copy .env.example .env
   ```

   On macOS or Linux, use `cp .env.example .env`.

4. Edit `.env` and set the values listed under Environment Variables below.
5. Start the app:

   ```
   python app.py
   ```

6. Open http://127.0.0.1:5000 in your browser.

---

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | A long random string. Required in production. Generate one with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | Database connection string. Use `sqlite:///cardwapas.db` locally, or your PostgreSQL URL in production |
| `BASE_URL` | Public address of the site, used inside QR codes. Use `http://127.0.0.1:5000` locally, or `https://hack4sdg-mindmeshh-1.onrender.com` on the live site, with no trailing slash |
| `MAIL_SERVER` | SMTP server, for example `smtp.gmail.com` (optional) |
| `MAIL_PORT` | SMTP port, for example `587` (optional) |
| `MAIL_USERNAME` | SMTP login. Leave empty to print emails to the console (optional) |
| `MAIL_PASSWORD` | SMTP password or Gmail App Password (optional) |
| `MAIL_SENDER` | Sender address for notification emails (optional) |

Never commit your `.env` file to Git.

### Email Notifications

If `MAIL_USERNAME` is empty, emails are printed to the console (or the Render **Logs** tab) instead of being sent, so the full flow can be demonstrated without an email account. To send real emails with Gmail, turn on 2-Step Verification, create an App Password, and put the credentials in `MAIL_USERNAME`, `MAIL_PASSWORD`, and `MAIL_SENDER`.

---

## Deployment

The app is deployed on Render with a PostgreSQL database.

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn "app:create_app()"`
- **Environment variables:** `SECRET_KEY`, `DATABASE_URL`, and `BASE_URL`, set in the Render dashboard.

After the first deploy, set `BASE_URL` to the address Render gives you, and generate new cards so their QR codes use it.

---

## Privacy and Responsible Technology

CardWapas is designed to protect both owners and finders.

- The QR code contains only a public recovery URL with a random token.
- The owner's phone number and email address are never displayed on the public found page.
- Passwords are securely hashed.
- Finder reports are protected by input validation and rate limiting.
- Finder contact information and location are optional.
- Meetups are intended to happen at safe, public locations.
- The finder is never asked for a home address.
- Secret keys and email credentials are stored in environment variables.
- HTTPS is required for deployment.
- Owners can deactivate or regenerate a card's QR token if it is misused.

**Privacy first:** CardWapas helps people reconnect without exposing personal information.

---

## Impact

CardWapas aims to measure its contribution through:

- Number of cards registered.
- Number of found reports received.
- Number of cards successfully recovered.
- Average time between a found report and recovery.

Every recovered card represents an opportunity to avoid unnecessary replacement and reduce waste.

---

## Testing and Demo

The project should be tested through the complete recovery workflow.

### End-to-End Test

1. Register a metro card owner.
2. Add a card and generate its QR code.
3. Print or display the QR code on a metro card.
4. Scan the QR code using another device.
5. Submit a found report as a finder.
6. Show the email notification received by the owner.
7. Open the owner dashboard and review the report.
8. Confirm the meetup.
9. Mark the card as recovered.
10. Show the updated recovery statistics.

### Success Criteria

- The complete recovery flow works without errors.
- A finder can submit a report in under 30 seconds.
- The owner receives a notification.
- Owner personal details remain hidden from public pages.
- The card can be marked as recovered.
- The demo can be completed within the presentation time.

---

## Future Scope

Potential improvements beyond the hackathon MVP:

- Integration with BMRCL for card verification and balance freezing.
- SMS or WhatsApp notifications.
- Anonymous in-app communication.
- NFC-based recovery tags.
- Support for city bus cards and other prepaid transit cards.
- Recovery support for other small personal items.
- Recovery analytics and heatmaps.
- Optional map-based meetup selection.
