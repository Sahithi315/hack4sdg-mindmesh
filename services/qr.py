"""QR code and sticker helpers.  OWNER: Person 4 (Integrations and demo)."""
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
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


def _get_font(size, bold=False):
    """Cross-platform font loader with graceful fallbacks."""
    candidates = (
        ["arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"]
        if bold
        else ["arial.ttf", "Arial.ttf", "DejaVuSans.ttf", "segoeui.ttf"]
    )
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def _draw_centered(draw, y, text, font, fill="#212529", width=380):
    """Draw a string centered horizontally at coordinate y."""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = max(8, (width - text_w) // 2)
    draw.text((x, y), text, fill=fill, font=font)
    return bbox[3] - bbox[1]


def generate_sticker_png(url, label="My metro card"):
    """Return a BytesIO PNG of a small printable sticker.

    Includes:
    - Card label at the top
    - Unique recovery QR code
    - Text: 'Found this card? Scan to return it to its owner'
    """
    width = 380
    height = 470

    img = Image.new("RGB", (width, height), "#ffffff")
    draw = ImageDraw.Draw(img)

    # Outer border (sticker cut line / badge border)
    draw.rounded_rectangle(
        [(8, 8), (width - 8, height - 8)], radius=14, outline="#0d6efd", width=3
    )

    # Header branding
    font_brand = _get_font(12, bold=True)
    _draw_centered(
        draw, 20, "CARDWAPAS • RECOVERY STICKER", font_brand, fill="#0d6efd", width=width
    )

    # Card label (truncated if too long to prevent overflowing sticker edge)
    display_label = (label or "My metro card").strip()
    font_label = _get_font(16, bold=True)
    while (
        draw.textbbox((0, 0), display_label, font=font_label)[2] > (width - 40)
        and len(display_label) > 3
    ):
        display_label = display_label[:-4] + "..."
    _draw_centered(draw, 42, display_label, font_label, fill="#212529", width=width)

    # Top divider
    draw.line([(30, 72), (width - 30, 72)], fill="#dee2e6", width=1)

    # QR Code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=6,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    if qr_img.width > 220:
        qr_img = qr_img.resize((220, 220), Image.Resampling.LANCZOS)

    qr_x = (width - qr_img.width) // 2
    qr_y = 86
    img.paste(qr_img, (qr_x, qr_y))

    # Divider below QR
    divider_y = qr_y + qr_img.height + 14
    draw.line([(30, divider_y), (width - 30, divider_y)], fill="#dee2e6", width=1)

    # Instructions for finder
    font_cta_bold = _get_font(15, bold=True)
    font_cta_sub = _get_font(13, bold=False)
    font_note = _get_font(10, bold=False)

    _draw_centered(draw, divider_y + 10, "Found this card?", font_cta_bold, fill="#0d6efd", width=width)
    _draw_centered(
        draw,
        divider_y + 32,
        "Scan to return it to its owner",
        font_cta_sub,
        fill="#212529",
        width=width,
    )
    _draw_centered(
        draw,
        divider_y + 56,
        "Safe & anonymous • No login needed",
        font_note,
        fill="#6c757d",
        width=width,
    )

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
