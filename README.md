# CardWapas
## QR-Based Lost Metro Card Recovery System

CardWapas is a web application that helps people recover lost prepaid metro cards using unique QR codes. Instead of losing the remaining balance or relying on slow metro lost-and-found processes, owners can receive recovery reports and coordinate a safe meetup with the finder.

**Built for a 24-hour hackathon**  
**Primary SDG:** SDG 9 — Industry, Innovation and Infrastructure (Target 9.c)  
**Secondary SDG:** SDG 12 — Responsible Consumption and Production (Target 12.5)

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

## Sustainable Development Goals

### SDG 9: Industry, Innovation and Infrastructure

CardWapas supports SDG 9, particularly target 9.c, by using accessible digital technology to solve an everyday transportation problem.

### SDG 12: Responsible Consumption and Production

CardWapas supports SDG 12, particularly target 12.5, by encouraging the recovery and reuse of existing metro cards. Recovering a lost card can help avoid unnecessary replacement cards and reduce plastic waste.

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

The owner dashboard is designed to display:

- Registered cards.
- Found reports.
- Recovery status.
- Recovered cards.
- Optional recovery analytics.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python 3 |
| Web Framework | Flask |
| Database | SQLite |
| ORM | Flask-SQLAlchemy |
| Authentication | Flask-Login |
| Password Security | Werkzeug password hashing |
| Frontend | HTML, CSS, Bootstrap 5 |
| Templates | Jinja2 |
| QR Code Generation | qrcode, Pillow |
| Email Notifications | Flask-Mail or smtplib |
| Rate Limiting | Flask-Limiter |
| Deployment | Render or PythonAnywhere |
| Version Control | Git, GitHub |

## System Architecture

```text
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
       SQLite Database
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

## Impact

CardWapas aims to measure its contribution through:

- Number of cards registered.
- Number of found reports received.
- Number of cards successfully recovered.
- Average time between a found report and recovery.

Every recovered card represents an opportunity to avoid unnecessary replacement and reduce waste.

## Testing and Demo

The project should be tested through the complete recovery workflow.

### End-to-End Demo

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
