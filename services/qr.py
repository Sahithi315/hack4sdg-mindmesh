"""QR code helpers.  OWNER: Person 4 (Integrations and demo)."""
from io import BytesIO

import qrcode
from flask import current_app, request


def build_found_url(token):
    """The public URL a finder lands on after scanning the QR.
    The QR contains ONLY this URL (a random token), never a login or personal data."""
    base = (current_app.config.get("BASE_URL") or request.url_root).rstrip("/")
    return f"{base}/found/{token}"


def generate_qr_png(url):
    """Return a BytesIO containing a PNG QR code for `url`.

    TODO (Person 4): make a printable sticker sheet (QR + the text
    "Found this card? Scan to return it to its owner") using Pillow.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
