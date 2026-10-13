#!/usr/bin/env python3
"""Build the final 60-page Crawling Bugs print interior for KDP."""
from __future__ import annotations

import csv
import re
from pathlib import Path

from PIL import Image
from pypdf import PdfReader
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from facts_v2 import fact_for

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "books/prompts/manifest-v2.csv"
SOURCE_ART = ROOT / "books/art/interior-v2/crawling-bugs"
PRINT_ART = ROOT / "books/art/print-art/crawling-bugs"
OUT = ROOT / "books/print-masters/crawling-bugs"
PDF = OUT / "crawling-bugs-interior-print-ready.pdf"
BRAND = ROOT / "brand/acornoodle"
CORPORATE_LOGO = BRAND / "corporate-logo-primary.png"
MASCOT_LINE_ART = BRAND / "mascot-reading-line-art.png"
W, H = 8.5 * 72, 11 * 72
THEME = HexColor("#5E8E3E")
REGULAR = "ArialEmbedded"
BOLD = "ArialBoldEmbedded"
pdfmetrics.registerFont(TTFont(REGULAR, "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont(BOLD, "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def source_for(row: dict[str, str]) -> Path:
    return SOURCE_ART / f"page-{int(row['page']):02d}-{slugify(row['object_name'])}.png"


def prepare_art(rows: list[dict[str, str]]) -> None:
    PRINT_ART.mkdir(parents=True, exist_ok=True)
    for row in rows:
        source = source_for(row)
        target = PRINT_ART / source.name
        if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
            continue
        with Image.open(source) as image:
            image = image.convert("L")
            image = image.resize((2550, 3300), Image.Resampling.LANCZOS)
            image.save(target, "PNG", optimize=True, dpi=(300, 300))


def fit_image(c: canvas.Canvas, path: Path, x: float, y: float, w: float, h: float) -> None:
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(str(path)), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, mask="auto")


def blank_back(c: canvas.Canvas) -> None:
    c.setFillColor(HexColor("#777777"))
    c.setFont(REGULAR, 7)
    # Keep the notice a full half-inch above trim so KDP's margin checker
    # does not flag the reverse pages as out of bounds.
    c.drawCentredString(W / 2, 36, "This page is intentionally blank to help prevent bleed-through.")
    c.showPage()


def title_page(c: canvas.Canvas) -> None:
    c.setFillColor(THEME)
    c.roundRect(54, H - 255, W - 108, 138, 24, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont(BOLD, 38)
    c.drawCentredString(W / 2, H - 180, "CRAWLING BUGS")
    c.setFont(BOLD, 17)
    c.drawCentredString(W / 2, H - 215, "A COLORING BOOK FOR AGES 5-9")
    c.setFillColor(black)
    c.setFont(BOLD, 14)
    c.drawCentredString(W / 2, 174, "26 BIG PICTURES WITH NAMES AND FUN FACTS")
    c.setFont(BOLD, 11)
    c.drawCentredString(W / 2, 153, "MARK NELSON")
    c.setFont(REGULAR, 8.5)
    c.drawCentredString(W / 2, 136, "ACORNOODLE DISCOVERY COLORING BOOKS")
    fit_image(c, CORPORATE_LOGO, W / 2 - 55, 25, 110, 105)
    c.showPage()


def copyright_page(c: canvas.Canvas) -> None:
    c.setFillColor(black)
    c.setFont(BOLD, 18)
    c.drawString(54, H - 82, "COPYRIGHT AND USE")
    c.setFont(REGULAR, 10)
    t = c.beginText(54, H - 116)
    t.setLeading(16)
    for line in [
        "Crawling Bugs: A Coloring Book for Ages 5-9",
        "Copyright (c) 2026 Nelson Grey LLC. All rights reserved.",
        "",
        "Published by Acornoodle Books, an imprint of Nelson Grey LLC.",
        "Author: Mark Nelson. Acornoodle Discovery Coloring Books series.",
        "First paperback edition, 2026.",
        "",
        "No part of this book may be reproduced, stored, or distributed in any form",
        "without prior written permission, except for brief quotations in reviews.",
        "Purchased copies may be colored for personal use.",
        "",
        "The illustrations were created with generative AI tools and were selected,",
        "reviewed, labeled, edited, and arranged by the publisher.",
        "",
        "For best results, place a protective sheet behind each page when using markers.",
        "Printed in the United States of America.",
    ]:
        t.textLine(line)
    c.drawText(t)
    c.showPage()


def belongs_page(c: canvas.Canvas) -> None:
    c.setFillColor(THEME)
    c.setFont(BOLD, 28)
    c.drawCentredString(W / 2, H * .69, "THIS BOOK BELONGS TO")
    c.setStrokeColor(black)
    c.setLineWidth(2)
    c.line(110, H * .57, W - 110, H * .57)
    c.setFillColor(black)
    c.setFont(REGULAR, 11)
    c.drawCentredString(W / 2, H * .52, "Write your name above and make this bug adventure your own!")
    fit_image(c, MASCOT_LINE_ART, W / 2 - 90, 80, 180, 250)
    c.showPage()


def color_test_page(c: canvas.Canvas) -> None:
    c.setFillColor(THEME)
    c.setFont(BOLD, 24)
    c.drawString(54, H - 78, "TRY YOUR COLORS")
    c.setFillColor(black)
    c.setFont(REGULAR, 11)
    c.drawString(54, H - 102, "Test crayons, colored pencils, or markers here before you begin.")
    c.setStrokeColor(black)
    for row in range(6):
        for col in range(5):
            c.circle(82 + col * 112, H - 170 - row * 88, 28, stroke=1, fill=0)
    c.showPage()


def coloring_page(c: canvas.Canvas, row: dict[str, str]) -> None:
    art = PRINT_ART / source_for(row).name
    fit_image(c, art, 45, 132, W - 90, H - 178)
    label = row["object_name"].upper()
    fact = fact_for("Crawling Bugs", row["object_name"])
    c.setFillColor(white)
    c.setStrokeColor(black)
    c.setLineWidth(1.6)
    c.setFont(BOLD, 20)
    text_width = c.stringWidth(label, BOLD, 20)
    box_width = min(W - 70, max(390, text_width + 50))
    c.roundRect((W - box_width) / 2, 33, box_width, 78, 12, stroke=1, fill=1)
    c.setFillColor(black)
    c.drawCentredString(W / 2, 78, label)
    c.setFont(REGULAR, 9.2)
    c.drawCentredString(W / 2, 53, fact)
    c.showPage()


def finish_pages(c: canvas.Canvas) -> None:
    c.setFillColor(THEME)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H * .66, "GREAT COLORING!")
    c.setFillColor(black)
    c.setFont(REGULAR, 14)
    c.drawCentredString(W / 2, H * .59, "You discovered 26 different crawling bugs.")
    c.setFont(BOLD, 13)
    c.drawCentredString(W / 2, H * .48, "My favorite bug was:")
    c.line(120, H * .42, W - 120, H * .42)
    fit_image(c, MASCOT_LINE_ART, W / 2 - 65, 72, 130, 200)
    c.showPage()
    blank_back(c)
    c.setFillColor(THEME)
    c.setFont(BOLD, 28)
    c.drawCentredString(W / 2, H * .66, "KEEP EXPLORING!")
    c.setFillColor(black)
    c.setFont(REGULAR, 13)
    c.drawCentredString(W / 2, H * .59, "How many of these amazing bugs can you spot outdoors?")
    c.setFont(BOLD, 12)
    c.drawCentredString(W / 2, H * .49, "LOOK GENTLY - WATCH CLOSELY - LEAVE WILD BUGS OUTSIDE")
    c.showPage()
    blank_back(c)


def main() -> None:
    rows = [r for r in csv.DictReader(MANIFEST.open()) if r["book_slug"] == "crawling-bugs"]
    assert len(rows) == 26
    prepare_art(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(PDF), pagesize=(W, H), pageCompression=1, initialFontName=REGULAR)
    c.setTitle("Crawling Bugs: A Coloring Book for Ages 5-9")
    c.setAuthor("Mark Nelson")
    c.setSubject("Children's coloring and nature activity book")
    c.setKeywords("bugs, coloring book, children, ages 5-9, insects, nature, fun facts")
    title_page(c)
    copyright_page(c)
    belongs_page(c)
    color_test_page(c)
    for row in rows:
        coloring_page(c, row)
        blank_back(c)
    finish_pages(c)
    c.save()
    reader = PdfReader(str(PDF))
    assert len(reader.pages) == 60
    assert all(float(p.mediabox.width) == W and float(p.mediabox.height) == H for p in reader.pages)
    print(PDF)


if __name__ == "__main__":
    main()
