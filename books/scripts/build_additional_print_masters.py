#!/usr/bin/env python3
"""Build branded 60-page KDP print interiors for selected Acornoodle titles."""
from __future__ import annotations

import csv
import re
import sys
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
BRAND = ROOT / "brand/acornoodle"
CORPORATE_LOGO = BRAND / "corporate-logo-primary.png"
MASCOT_LINE_ART = BRAND / "mascot-reading-line-art.png"
W, H = 8.5 * 72, 11 * 72
REGULAR = "ArialEmbedded"
BOLD = "ArialBoldEmbedded"
pdfmetrics.registerFont(TTFont(REGULAR, "/System/Library/Fonts/Supplemental/Arial.ttf"))
pdfmetrics.registerFont(TTFont(BOLD, "/System/Library/Fonts/Supplemental/Arial Bold.ttf"))

BOOKS = {
    "roaring-dinosaurs": {
        "title": "Roaring Dinosaurs",
        "theme": "#6A8F3D",
        "adventure": "dinosaur adventure",
        "plural": "incredible dinosaurs",
        "favorite": "dinosaur",
        "question": "Which amazing dinosaurs would you like to discover next?",
        "closing": "STAY CURIOUS - KEEP DISCOVERING - LET YOUR IMAGINATION ROAR",
        "subject": "Children's dinosaur coloring and science activity book",
        "keywords": "dinosaurs, coloring book, children, ages 5-9, prehistoric animals, fun facts",
    },
    "working-vehicles": {
        "title": "Working Vehicles",
        "theme": "#E0A20B",
        "adventure": "vehicle adventure",
        "plural": "hardworking vehicles",
        "favorite": "vehicle",
        "question": "How many of these hardworking vehicles can you spot nearby?",
        "closing": "LOOK CLOSELY - ASK QUESTIONS - DISCOVER HOW THINGS WORK",
        "subject": "Children's vehicle coloring and early engineering activity book",
        "keywords": "vehicles, coloring book, children, ages 5-9, trucks, machines, fun facts",
    },
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def fit_image(c: canvas.Canvas, path: Path, x: float, y: float, w: float, h: float) -> None:
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(str(path)), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, mask="auto")


def build(slug: str) -> Path:
    cfg = BOOKS[slug]
    rows = [r for r in csv.DictReader(MANIFEST.open()) if r["book_slug"] == slug]
    assert len(rows) == 26
    source_art = ROOT / "books/art/interior-v2" / slug
    print_art = ROOT / "books/art/print-art" / slug
    out = ROOT / "books/print-masters" / slug
    pdf = out / f"{slug}-interior-print-ready.pdf"
    theme = HexColor(cfg["theme"])
    print_art.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)

    def source_for(row: dict[str, str]) -> Path:
        return source_art / f"page-{int(row['page']):02d}-{slugify(row['object_name'])}.png"

    for row in rows:
        source = source_for(row)
        target = print_art / source.name
        if not target.exists() or target.stat().st_mtime < source.stat().st_mtime:
            with Image.open(source) as image:
                image.convert("L").resize((2550, 3300), Image.Resampling.LANCZOS).save(
                    target, "PNG", optimize=True, dpi=(300, 300)
                )

    c = canvas.Canvas(str(pdf), pagesize=(W, H), pageCompression=1, initialFontName=REGULAR)
    c.setTitle(f"{cfg['title']}: A Coloring Book for Ages 5-9")
    c.setAuthor("Mark Nelson")
    c.setSubject(cfg["subject"])
    c.setKeywords(cfg["keywords"])

    # Title page
    c.setFillColor(theme)
    c.roundRect(54, H - 255, W - 108, 138, 24, fill=1, stroke=0)
    c.setFillColor(white)
    title_size = 38
    while c.stringWidth(cfg["title"].upper(), BOLD, title_size) > W - 140:
        title_size -= 1
    c.setFont(BOLD, title_size)
    c.drawCentredString(W / 2, H - 180, cfg["title"].upper())
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

    # Copyright page
    c.setFillColor(black)
    c.setFont(BOLD, 18)
    c.drawString(54, H - 82, "COPYRIGHT AND USE")
    c.setFont(REGULAR, 10)
    t = c.beginText(54, H - 116)
    t.setLeading(16)
    for line in [
        f"{cfg['title']}: A Coloring Book for Ages 5-9",
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

    # Ownership page
    c.setFillColor(theme)
    c.setFont(BOLD, 28)
    c.drawCentredString(W / 2, H * .69, "THIS BOOK BELONGS TO")
    c.setStrokeColor(black)
    c.setLineWidth(2)
    c.line(110, H * .57, W - 110, H * .57)
    c.setFillColor(black)
    c.setFont(REGULAR, 11)
    c.drawCentredString(W / 2, H * .52, f"Write your name above and make this {cfg['adventure']} your own!")
    fit_image(c, MASCOT_LINE_ART, W / 2 - 90, 80, 180, 250)
    c.showPage()

    # Color test page
    c.setFillColor(theme)
    c.setFont(BOLD, 24)
    c.drawString(54, H - 78, "TRY YOUR COLORS")
    c.setFillColor(black)
    c.setFont(REGULAR, 11)
    c.drawString(54, H - 102, "Test crayons, colored pencils, or markers here before you begin.")
    c.setStrokeColor(black)
    for r in range(6):
        for col in range(5):
            c.circle(82 + col * 112, H - 170 - r * 88, 28, stroke=1, fill=0)
    c.showPage()

    def blank_back() -> None:
        c.setFillColor(HexColor("#777777"))
        c.setFont(REGULAR, 7)
        c.drawCentredString(W / 2, 36, "This page is intentionally blank to help prevent bleed-through.")
        c.showPage()

    # Coloring pages and safe reverse pages
    for row in rows:
        art = print_art / source_for(row).name
        fit_image(c, art, 45, 132, W - 90, H - 178)
        label = row["object_name"].upper()
        fact = row["fact"]
        c.setFillColor(white)
        c.setStrokeColor(black)
        c.setLineWidth(1.6)
        c.setFont(BOLD, 20)
        text_width = c.stringWidth(label, BOLD, 20)
        box_width = min(W - 70, max(390, text_width + 50))
        c.roundRect((W - box_width) / 2, 33, box_width, 78, 12, stroke=1, fill=1)
        c.setFillColor(black)
        c.drawCentredString(W / 2, 78, label)
        fact_size = 9.2
        while c.stringWidth(fact, REGULAR, fact_size) > box_width - 28 and fact_size > 7.2:
            fact_size -= .2
        c.setFont(REGULAR, fact_size)
        c.drawCentredString(W / 2, 53, fact)
        c.showPage()
        blank_back()

    # Completion and closing pages
    c.setFillColor(theme)
    c.setFont(BOLD, 30)
    c.drawCentredString(W / 2, H * .66, "GREAT COLORING!")
    c.setFillColor(black)
    c.setFont(REGULAR, 14)
    c.drawCentredString(W / 2, H * .59, f"You discovered 26 {cfg['plural']}.")
    c.setFont(BOLD, 13)
    c.drawCentredString(W / 2, H * .48, f"My favorite {cfg['favorite']} was:")
    c.line(120, H * .42, W - 120, H * .42)
    fit_image(c, MASCOT_LINE_ART, W / 2 - 65, 72, 130, 200)
    c.showPage()
    blank_back()
    c.setFillColor(theme)
    c.setFont(BOLD, 28)
    c.drawCentredString(W / 2, H * .66, "KEEP EXPLORING!")
    c.setFillColor(black)
    c.setFont(REGULAR, 13)
    c.drawCentredString(W / 2, H * .59, cfg["question"])
    c.setFont(BOLD, 11)
    c.drawCentredString(W / 2, H * .49, cfg["closing"])
    c.showPage()
    blank_back()
    c.save()

    reader = PdfReader(str(pdf))
    assert len(reader.pages) == 60
    assert all(float(p.mediabox.width) == W and float(p.mediabox.height) == H for p in reader.pages)
    return pdf


def main() -> None:
    slugs = sys.argv[1:] or list(BOOKS)
    for slug in slugs:
        if slug not in BOOKS:
            raise SystemExit(f"Unknown book: {slug}")
        print(build(slug))


if __name__ == "__main__":
    main()
