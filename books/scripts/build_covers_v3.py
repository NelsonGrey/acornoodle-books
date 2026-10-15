#!/usr/bin/env python3
"""Build the full-color V3 KDP cover wraps and pair them with V2 interiors."""
from __future__ import annotations

import csv
import shutil
from pathlib import Path

from PIL import Image
from pypdf import PdfReader
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "books/prompts/manifest-v2.csv"
ART = ROOT / "books/art/cover-v3"
PRINT_ART = ROOT / "books/art/cover-v3-print"
BRAND = ROOT / "brand/acornoodle"
CORPORATE_LOGO = BRAND / "corporate-logo-primary.png"
COVER_IDENTITY = BRAND / "cover-identity-primary.png"
OLD = ROOT / "books/archive/final-kids-v2"
OUT = ROOT / "books/builds/final-kids-v3"

PAGE_COUNT = 60
SPINE = PAGE_COUNT * .002252 * 72
COVER_W, COVER_H = 17.25 * 72 + SPINE, 11.25 * 72
BLEED = .125 * 72
PANEL_W = 8.5 * 72
FRONT_X = BLEED + PANEL_W + SPINE
REGULAR = "ArialEmbedded"
BOLD = "ArialBoldEmbedded"
pdfmetrics.registerFont(TTFont(REGULAR, "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont(BOLD, "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

NOUNS = {
    "crawling-bugs": "crawling bugs",
    "flying-bugs": "flying bugs",
    "singing-birds": "singing birds",
    "soaring-birds": "soaring birds",
    "schools-of-fish": "schools of fish",
    "lonely-fish": "fascinating fish",
    "roaring-dinosaurs": "roaring dinosaurs",
    "sleepy-dinosaurs": "sleepy dinosaurs",
    "busy-farm-animals": "busy farm animals",
    "cuddly-farm-animals": "cuddly farm animals",
    "working-vehicles": "working vehicles",
    "racing-vehicles": "racing vehicles",
}


def crop_fill(c: canvas.Canvas, path: Path, x: float, y: float, w: float, h: float) -> None:
    with Image.open(path) as im:
        iw, ih = im.size
    scale = max(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y, w, h)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(ImageReader(str(path)), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh)
    c.restoreState()


def prepare_cover_art(book: str) -> Path:
    source = ART / f"{book}.png"
    target = PRINT_ART / f"{book}.png"
    PRINT_ART.mkdir(parents=True, exist_ok=True)
    if not target.exists() or target.stat().st_mtime < source.stat().st_mtime:
        with Image.open(source) as image:
            image = image.convert("RGB").resize((2700, 3375), Image.Resampling.LANCZOS)
            image.save(target, "PNG", optimize=True, dpi=(300, 300))
    return target


def title_lines(title: str) -> list[str]:
    words = title.upper().split()
    if len(words) <= 2:
        return [" ".join(words)]
    best = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
    return [" ".join(words[:best]), " ".join(words[best:])]


def centered_fit(c: canvas.Canvas, text: str, x: float, y: float, width: float, start: float) -> None:
    size = start
    while c.stringWidth(text, BOLD, size) > width and size > 18:
        size -= 1
    c.setFont(BOLD, size)
    c.drawCentredString(x, y, text)


def contain_image(c: canvas.Canvas, path: Path, x: float, y: float, w: float, h: float) -> None:
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(
        ImageReader(str(path)), x + (w - dw) / 2, y + (h - dh) / 2,
        dw, dh, mask="auto",
    )


def build_cover(book: str, title: str, color: str) -> Path:
    art = prepare_cover_art(book)
    path = OUT / f"{book}-cover-full-wrap-v3.pdf"
    c = canvas.Canvas(str(path), pagesize=(COVER_W, COVER_H), pageCompression=1, initialFontName=REGULAR)
    c.setTitle(f"{title} - Full Color Cover")
    c.setAuthor("Nelson Grey LLC")
    theme = HexColor(color)

    # Back, spine, and a full-bleed illustrated front.
    c.setFillColor(theme)
    c.rect(0, 0, COVER_W, COVER_H, fill=1, stroke=0)
    crop_fill(c, art, FRONT_X, 0, PANEL_W + BLEED, COVER_H)

    # Front title card and badges stay readable in Amazon thumbnail views.
    c.setFillColor(theme)
    c.roundRect(FRONT_X + 30, COVER_H - 174, PANEL_W - 60, 132, 22, fill=1, stroke=0)
    c.setFillColor(white)
    lines = title_lines(title)
    if len(lines) == 1:
        centered_fit(c, lines[0], FRONT_X + PANEL_W / 2, COVER_H - 125, PANEL_W - 90, 39)
    else:
        centered_fit(c, lines[0], FRONT_X + PANEL_W / 2, COVER_H - 105, PANEL_W - 90, 34)
        centered_fit(c, lines[1], FRONT_X + PANEL_W / 2, COVER_H - 145, PANEL_W - 90, 34)

    c.setFillColor(white)
    c.roundRect(FRONT_X + PANEL_W / 2 - 72, COVER_H - 210, 144, 28, 10, fill=1, stroke=0)
    c.setFillColor(theme)
    c.setFont(BOLD, 10.5)
    c.drawCentredString(FRONT_X + PANEL_W / 2, COVER_H - 200, "BY MARK NELSON")

    c.setFillColor(white)
    c.roundRect(FRONT_X + 48, 22, PANEL_W - 96, 142, 18, fill=1, stroke=0)
    c.setFillColor(theme)
    c.setFont(BOLD, 15)
    c.drawCentredString(FRONT_X + PANEL_W / 2, 147, "26 BIG PICTURES - NAMES - FUN FACTS")
    c.setFont(BOLD, 13)
    c.drawCentredString(FRONT_X + PANEL_W / 2, 128, "A COLORING BOOK FOR AGES 5-9")
    contain_image(c, COVER_IDENTITY, FRONT_X + PANEL_W / 2 - 110, 27, 220, 94)

    # KDP does not permit spine text on paperbacks under 79 pages.

    # Back-cover information panel.
    info_lines = [
        f"Meet 26 different {NOUNS[book]} in a book",
        "made especially for young artists.",
        "",
        "Every illustration includes its name and a fun fact.",
        "Large subjects and bold outlines make coloring inviting.",
        "",
        "INSIDE:",
        "- 26 unique pictures",
        "- Simple, child-friendly backgrounds",
        "- Single-sided coloring pages",
        "- Large 8.5 x 11 inch format",
    ]
    # Trim the card from the right to fit its widest line (left edge and height stay put).
    headline = "COLOR. LEARN. DISCOVER."
    content_w = max(
        c.stringWidth(headline, BOLD, 24),
        max(c.stringWidth(line, REGULAR, 12) for line in info_lines),
        180,  # AGES badge
    )
    c.setFillColor(white)
    c.roundRect(38, 156, 26 + content_w + 26, COVER_H - 210, 24, fill=1, stroke=0)
    c.setFillColor(theme)
    c.setFont(BOLD, 24)
    c.drawString(64, COVER_H - 88, headline)
    c.setFillColor(black)
    c.setFont(REGULAR, 12)
    t = c.beginText(64, COVER_H - 128)
    t.setLeading(18)
    for line in info_lines:
        t.textLine(line)
    c.drawText(t)

    c.setFillColor(theme)
    c.roundRect(64, 182, 180, 48, 12, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(BOLD, 16)
    c.drawCentredString(154, 199, "AGES 5-9")

    # The corporate logo sits on a white panel so it reads on every cover color.
    barcode_x = BLEED + PANEL_W - 18 - 144
    imprint = "An imprint of Nelson Grey LLC"
    site = "acornoodlebooks.com"
    text_w = max(c.stringWidth(imprint, REGULAR, 8.5), c.stringWidth(site, BOLD, 10.5))
    c.setFillColor(white)
    c.roundRect(38, 22, 176 + text_w + 26 - 38, 126, 18, fill=1, stroke=0)
    contain_image(c, CORPORATE_LOGO, 52, 30, 108, 108)
    c.setFillColor(black)
    c.setFont(REGULAR, 8.5)
    c.drawString(176, 84, imprint)
    c.setFont(BOLD, 10.5)
    c.drawString(176, 68, site)

    # Reserved KDP barcode area on the lower back cover.
    c.setFillColor(white)
    c.rect(barcode_x, 50, 144, 86, fill=1, stroke=0)
    c.save()
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(MANIFEST.open()))
    books: dict[str, dict[str, str]] = {}
    for row in rows:
        books.setdefault(row["book_slug"], row)
    for book, row in books.items():
        if not (ART / f"{book}.png").exists():
            raise FileNotFoundError(ART / f"{book}.png")
        build_cover(book, row["book_title"], row["cover_color"])
        source = OLD / f"{book}-interior-8.5x11.pdf"
        shutil.copy2(source, OUT / source.name)
    for pdf in OUT.glob("*.pdf"):
        expected = 60 if "interior" in pdf.name else 1
        assert len(PdfReader(str(pdf)).pages) == expected, pdf
    print(f"Built {len(books)} V3 covers and paired interiors in {OUT}")


if __name__ == "__main__":
    main()
