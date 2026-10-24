# Product Requirements Document (PRD)

**Project (working title):** CardWapas, a QR-based lost metro card recovery system
**Context:** 24-hour hackathon
**Primary SDG:** SDG 12, Responsible Consumption and Production (target 12.5, waste reduction through reuse)
**Secondary SDG:** SDG 9, Industry, Innovation and Infrastructure (target 9.c, using technology to solve everyday problems)

---

## 1. Overview

Prepaid metro cards are anonymous. If one is lost, its balance is lost with it, and the owner has no way to be contacted. Recovery through the metro organization is slow, unreliable, or ignored.

CardWapas is a small web app. The owner sticks a unique QR code on their metro card. Anyone who finds the card scans the QR, with no app install or login, and sends the owner an anonymous notification with a proposed meetup point. The card goes straight from finder to owner, with no third-party organization involved.

## 2. Problem Statement

- Lost metro cards cannot be traced, blocked, or returned because they carry no owner information.
- Writing a phone number on the card exposes personal data and cannot be updated or revoked.
- Metro lost-and-found processes are slow, manual, and have no digital record.
- Replaced cards add plastic and e-waste that recovery would avoid.

## 3. Goals

1. Let an owner register a card and receive a printable QR in under 2 minutes.
2. Let a finder report a found card in under 30 seconds with no login.
3. Keep the owner's personal details (phone, email) hidden from finders at all times.
4. Notify the owner promptly and let both sides agree on a safe meetup.
5. Show simple impact numbers (cards registered, found, recovered).

## 4. Non-Goals (out of scope for the hackathon)

- Integration with BMRCL or any metro backend (no balance freezing or card-number lookup).
- Real-time tracking or proximity alerts (rejected earlier because of false positives).
- SMS notifications, in-app chat, and a native mobile app.
- Payments or rewards for finders.

## 5. Target Users

| User | Description | Needs |
|---|---|---|
| Owner | Daily metro commuter or student with a prepaid card | Get the card back safely without exposing personal data |
| Finder | Anyone who finds a card (often a fellow student or commuter) | Return it quickly with minimal effort and no sign-up |

Pilot audience: RVCE students first, then wider metro commuters.

## 6. User Stories

**Owner**
- I can sign up and log in securely.
- I can add a card (with an optional label like "Blue card") and get a unique QR to print.
- I can see all my cards and mark one as lost or active.
- I get an email when someone reports my card found.
- I can view the report (finder message, meetup point) and confirm or suggest a different meetup.
- I can mark the card as recovered.

**Finder**
- I can scan the QR and land on a simple page with no login.
- I can pick a meetup point from a preset list and add a short note.
- I can optionally leave a contact method or share my location.
- I can see a confirmation and check the owner's response through a private link.

## 7. Features

### MVP (must build in 24 hours)
1. Owner registration and login (hashed passwords, sessions).
2. Add card: unique random token and a downloadable QR PNG.
3. Public found page at `/found/<token>`.
4. Found report submission (message, preset meetup point, free-text note).
5. Email notification to the owner.
6. Owner dashboard: cards list and reports list.
7. "Mark as recovered" button.

### Nice-to-have (cut in this order if short on time)
1. Basic analytics counters on the dashboard.
2. Finder status page showing the owner's response.
3. Optional map pin (Leaflet + OpenStreetMap).
4. Printable sticker sheet (QR plus "Found me? Scan to return").
5. CAPTCHA on the found page.

## 8. User Flows

**Owner flow**
1. Sign up and log in.
2. Add a card, and the system generates a token and QR.
3. Print the QR and stick it on the card.

**Finder flow**
1. Scan the QR, which opens `/found/<token>`.
2. Choose a meetup point and write a short note.
3. Submit. The finder sees a confirmation and a private status link.

**Notification and handoff flow**
1. The server saves the report and emails the owner (without finder details beyond what the finder chose to share).
2. The owner opens the dashboard, reviews the report, and confirms or suggests another meetup.
3. They meet in a public place and the owner clicks "Mark as recovered."

## 9. Meetup Design

- Preset safe public points (for example: RVCE main gate, library entrance, metro station concourse public area), plus a free-text note.
- Optional map pin with Leaflet and OpenStreetMap (free, no billing account needed, unlike Google Maps).
- The finder is never asked for a home address. All communication goes through the app.
- Dropping the card at a metro station is intentionally not the default, since the project aims to avoid metro-organization involvement.

## 10. Technical Stack

| Layer | Choice | Why |
|---|---|---|
| Backend | Python 3 with Flask | Small, quick to learn, good for a 24-hour build |
| Database | SQLite (dev and demo), optional PostgreSQL later | Zero setup |
| ORM | Flask-SQLAlchemy | Simple models and queries |
| Auth | Flask-Login, passwords hashed with Werkzeug (`generate_password_hash`) or bcrypt | Standard, secure |
| Templates and UI | Jinja2, HTML, CSS, Bootstrap 5 | No separate frontend build needed |
| QR generation | `qrcode` with `Pillow` | One-line QR images |
| Token generation | Python `secrets.token_urlsafe(16)` | Long, unguessable URLs |
| Email | Flask-Mail or `smtplib` with Gmail SMTP (app password) | Free and quick to set up |
| Rate limiting | Flask-Limiter | Stops spam reports |
| Maps (optional) | Leaflet.js with OpenStreetMap | Free |
| Hosting | Render or PythonAnywhere, with gunicorn | HTTPS provided, needed for geolocation |
| Version control | Git and GitHub | Teamwork and deployment |

## 11. Data Model

**User**
- `id`, `name`, `email` (unique), `phone` (optional), `password_hash`, `created_at`

**Card**
- `id`, `owner_id` (FK), `label`, `token` (unique, indexed), `status` (`active`, `lost`, `recovered`), `created_at`

**FoundReport**
- `id`, `card_id` (FK), `message`, `meetup_point`, `meetup_note`, `finder_contact` (optional), `latitude` and `longitude` (optional), `report_token` (unique, for the finder's private status page), `status` (`new`, `owner_replied`, `recovered`), `owner_reply`, `created_at`, `recovered_at`

## 12. Routes

| Method | Route | Access | Purpose |
|---|---|---|---|
| GET/POST | `/register` | Public | Owner sign-up |
| GET/POST | `/login` | Public | Owner login |
| GET | `/logout` | Owner | Log out |
| GET | `/dashboard` | Owner | Cards, reports, analytics |
| POST | `/cards/add` | Owner | Create card and token |
| GET | `/cards/<id>/qr.png` | Owner | Download QR image |
| POST | `/cards/<id>/status` | Owner | Mark lost or active |
| GET/POST | `/found/<token>` | Public (rate limited) | Finder report page |
| GET | `/report/<report_token>` | Public (private link) | Finder's status page |
| POST | `/reports/<id>/reply` | Owner | Confirm or suggest meetup |
| POST | `/reports/<id>/recover` | Owner | Mark recovered |

## 13. Security and Privacy Requirements

- The QR encodes only a public URL with a random token. It never carries a login session or personal data.
- Tokens are at least 16 random bytes (unguessable).
- The found page never shows the owner's name, phone, or email.
- Passwords are hashed and never stored in plain text.
- All pages are served over HTTPS in deployment.
- Rate limiting on `/found/<token>` (for example, 5 reports per hour per IP) and optional CAPTCHA.
- Input validation and escaping on all finder text (use Jinja auto-escaping to prevent XSS).
- Secret keys and email credentials live in environment variables, not in the repo.
- Owner can deactivate or regenerate a card's token if the QR is misused.

## 14. Analytics (optional dashboard counters)

- Cards registered
- Found reports received
- Cards recovered
- Average time from report to recovery

## 15. 24-Hour Timeline

| Hours | Milestone |
|---|---|
| 0-2 | Project setup, repo, database models, agree on flow |
| 2-6 | Owner register and login, dashboard shell |
| 6-9 | Add card, token generation, QR download |
| 9-13 | Public found page and report submission |
| 13-16 | Email notification to owner |
| 16-19 | Owner reply and "Mark as recovered" |
| 19-21 | Analytics counters and meetup note polish |
| 21-24 | Deploy, end-to-end test with a real printed QR, prepare demo |

## 16. Demo Plan

1. Show the problem in one sentence: lost metro card, lost money, no way to reach the owner.
2. Register as an owner, add a card, and print or show the QR on a real card.
3. A teammate scans it on their phone, picks a meetup point, and submits.
4. The owner's phone shows the email live, then the owner confirms on the dashboard.
5. Mark as recovered and show the analytics counter updating.
6. Close with the SDG 12 angle: every recovered card is one fewer replacement card manufactured.

## 17. Success Metrics

- Full flow works end to end (scan, report, notification, recovery) without errors.
- Found report submits in under 30 seconds.
- Owner details never appear on any public page.
- Demo completes live within the presentation time.

## 18. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Email delivery is slow or fails during the demo | Show reports on the owner dashboard as a backup |
| Spam reports on a QR | Rate limiting, CAPTCHA, token regeneration |
| Finder never scans or never responds | Scope accepted: the system helps willing finders, it does not force returns |
| Unsafe meetups | Preset public meetup points only, no home addresses |
| Running out of time | Cut nice-to-haves in the order listed in section 7 |
| Dishonest claimant | Only the registered owner receives the report and can confirm the meetup |

## 19. Future Scope

- BMRCL integration for card-number verification and balance freezing.
- SMS or WhatsApp notifications.
- Anonymous in-app chat between finder and owner.
- NFC tag option in place of QR.
- Extension to other prepaid transit cards (city buses) and other small items (ID cards, keys).
- Larger-scale recovery analytics and heatmaps of where cards are lost.
