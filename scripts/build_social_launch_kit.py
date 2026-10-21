#!/usr/bin/env python3
"""Build the Acornoodle Books launch social-image kit from approved assets."""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "marketing" / "social-launch-2026-10-20" / "images"

FORMATS = {
    "pinterest": (1000, 1500),
    "instagram": (1080, 1350),
    "facebook": (1200, 1500),
}

CREAM = "#FFF6DF"
NAVY = "#123B63"
GREEN = "#579447"
GOLD = "#E8A11A"
RASPBERRY = "#D81B60"
SKY = "#299ED5"
WHITE = "#FFFFFF"
MUTED = "#426079"

FONT_REGULAR = Path("/System/Library/Fonts/Supplemental/Verdana.ttf")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Verdana Bold.ttf")

BOOKS = {
    "crawling-bugs": {
        "title": "CRAWLING BUGS",
        "kicker": "LOOK CLOSELY",
        "line": "Ants, beetles, caterpillars\nand garden neighbors",
        "color": GREEN,
        "cover": ROOT / "website/dist/assets/crawling-bugs-cover.png",
        "interior": ROOT / "books/art/interior-v2/crawling-bugs/page-03-seven-spotted-lady-beetle.png",
    },
    "roaring-dinosaurs": {
        "title": "ROARING DINOSAURS",
        "kicker": "TRAVEL WAY BACK",
        "line": "Famous giants and surprising\nprehistoric discoveries",
        "color": "#669638",
        "cover": ROOT / "website/dist/assets/roaring-dinosaurs-cover.png",
        "interior": ROOT / "books/art/interior-v2/roaring-dinosaurs/page-01-tyrannosaurus-rex.png",
        "interior_fit": "inset",
    },
    "working-vehicles": {
        "title": "WORKING VEHICLES",
        "kicker": "SEE HOW THINGS WORK",
        "line": "Machines that build, rescue,\nfarm, lift, and move",
        "color": GOLD,
        "cover": ROOT / "website/dist/assets/working-vehicles-cover.png",
        "interior": ROOT / "books/art/interior-v2/working-vehicles/page-01-excavator.png",
    },
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REGULAR), size)


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius, fill=255)
    return mask


def fit_image(path: Path, box: tuple[int, int], contain: bool = True, crop_anchor: str = "center") -> Image.Image:
    image = Image.open(path).convert("RGBA")
    if contain:
        image.thumbnail(box, Image.Resampling.LANCZOS)
        return image
    target_ratio = box[0] / box[1]
    ratio = image.width / image.height
    if ratio > target_ratio:
        new_width = int(image.height * target_ratio)
        x = (image.width - new_width) // 2
        image = image.crop((x, 0, x + new_width, image.height))
    else:
        new_height = int(image.width / target_ratio)
        if crop_anchor == "top":
            y = 0
        elif crop_anchor == "bottom":
            y = image.height - new_height
        else:
            y = (image.height - new_height) // 2
        image = image.crop((0, y, image.width, y + new_height))
    return image.resize(box, Image.Resampling.LANCZOS)


def paste_shadow(canvas: Image.Image, art: Image.Image, xy: tuple[int, int], radius: int = 24) -> None:
    x, y = xy
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer = Image.new("RGBA", art.size, (0, 0, 0, 150))
    shadow.paste(layer, (x + 12, y + 18), art.getchannel("A"))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius))
    canvas.alpha_composite(shadow)
    canvas.alpha_composite(art, (x, y))


def paste_center(canvas: Image.Image, image: Image.Image, y: int) -> None:
    canvas.alpha_composite(image, ((canvas.width - image.width) // 2, y))


def add_logo(canvas: Image.Image, top: int, max_width: int, panel: bool = False) -> None:
    logo = fit_image(ROOT / "brand/acornoodle/cover-identity-primary.png", (max_width, 170))
    if panel:
        pad_x = max(24, int(canvas.width * 0.025))
        pad_y = max(12, int(canvas.height * 0.010))
        left = (canvas.width - logo.width) // 2 - pad_x
        right = (canvas.width + logo.width) // 2 + pad_x
        ImageDraw.Draw(canvas).rounded_rectangle(
            (left, top - pad_y, right, top + logo.height + pad_y),
            radius=max(20, int(canvas.width * 0.025)),
            fill=CREAM,
        )
    paste_center(canvas, logo, top)


def dotted_background(canvas: Image.Image, color: str) -> None:
    draw = ImageDraw.Draw(canvas)
    for y in range(30, canvas.height, 80):
        for x in range(30 + (y // 80 % 2) * 35, canvas.width, 80):
            draw.ellipse((x, y, x + 8, y + 8), fill=color)


def draw_centered(draw: ImageDraw.ImageDraw, text: str, y: int, fnt: ImageFont.FreeTypeFont, fill: str, width: int) -> int:
    box = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=10, align="center")
    x = (width - (box[2] - box[0])) // 2
    draw.multiline_text((x, y), text, font=fnt, fill=fill, spacing=10, align="center")
    return y + (box[3] - box[1])


def draw_centered_in(draw: ImageDraw.ImageDraw, text: str, box: tuple[int, int, int, int], fnt: ImageFont.FreeTypeFont, fill: str) -> None:
    left, top, right, _bottom = box
    bounds = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=8, align="center")
    text_width = bounds[2] - bounds[0]
    draw.multiline_text((left + (right - left - text_width) // 2, top), text, font=fnt, fill=fill, spacing=8, align="center")


def launch_trio(size: tuple[int, int]) -> Image.Image:
    w, h = size
    canvas = Image.new("RGBA", size, CREAM)
    dotted_background(canvas, "#E9DDBD")
    draw = ImageDraw.Draw(canvas)
    add_logo(canvas, int(h * 0.035), int(w * 0.48))
    y = int(h * 0.16)
    y = draw_centered(draw, "THREE WAYS\nTO WONDER", y, font(int(w * 0.07), True), NAVY, w)
    draw_centered(draw, "The first Acornoodle Discovery Coloring Books", y + 20, font(int(w * 0.025)), MUTED, w)

    cover_w = int(w * 0.29)
    cover_h = int(cover_w * 1.293)
    gap = int(w * 0.025)
    total = cover_w * 3 + gap * 2
    start_x = (w - total) // 2
    cover_y = int(h * 0.37)
    for idx, data in enumerate(BOOKS.values()):
        cover = fit_image(data["cover"], (cover_w, cover_h))
        mask = rounded_mask(cover.size, 18)
        cover.putalpha(mask)
        paste_shadow(canvas, cover, (start_x + idx * (cover_w + gap), cover_y), 18)

    pill_w, pill_h = int(w * 0.56), int(h * 0.052)
    pill_x, pill_y = (w - pill_w) // 2, int(h * 0.82)
    draw.rounded_rectangle((pill_x, pill_y, pill_x + pill_w, pill_y + pill_h), pill_h // 2, fill=NAVY)
    label = "AVAILABLE NOW ON AMAZON"
    label_font = font(int(w * 0.026), True)
    label_box = draw.textbbox((0, 0), label, font=label_font)
    draw.text(((w - (label_box[2] - label_box[0])) // 2, pill_y + (pill_h - (label_box[3] - label_box[1])) // 2 - 2), label, font=label_font, fill=WHITE)
    draw_centered(draw, "Ages 5–9  •  26 pictures  •  Names + fun facts", int(h * 0.89), font(int(w * 0.024)), NAVY, w)
    draw_centered(draw, "acornoodlebooks.com", int(h * 0.94), font(int(w * 0.024), True), RASPBERRY, w)
    return canvas


def book_spotlight(size: tuple[int, int], data: dict[str, object]) -> Image.Image:
    w, h = size
    color = str(data["color"])
    canvas = Image.new("RGBA", size, CREAM)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, w, int(h * 0.30)), fill=color)
    dotted_background(canvas, "#E9DDBD")
    add_logo(canvas, int(h * 0.035), int(w * 0.42), panel=True)

    kicker_font = font(int(w * 0.026), True)
    kicker = str(data["kicker"])
    kb = draw.textbbox((0, 0), kicker, font=kicker_font)
    draw.text(((w - (kb[2] - kb[0])) // 2, int(h * 0.17)), kicker, font=kicker_font, fill=WHITE)
    draw_centered(draw, str(data["title"]), int(h * 0.21), font(int(w * 0.052), True), WHITE, w)

    cover_w = int(w * 0.47)
    cover_h = int(cover_w * 1.293)
    cover = fit_image(Path(data["cover"]), (cover_w, cover_h))
    cover.putalpha(rounded_mask(cover.size, 22))
    cover_x = int(w * 0.08)
    cover_y = int(h * 0.35)
    paste_shadow(canvas, cover, (cover_x, cover_y), 22)

    sample_size = int(w * 0.35)
    if data.get("interior_fit") == "inset":
        # Preserve the dinosaur's entire head and snout inside the circular frame.
        sample = Image.new("RGBA", (sample_size, sample_size), WHITE)
        inset = fit_image(
            Path(data["interior"]),
            (int(sample_size * 0.82), int(sample_size * 1.08)),
            contain=True,
        )
        sample.alpha_composite(inset, ((sample_size - inset.width) // 2, int(sample_size * 0.035)))
    else:
        sample = fit_image(
            Path(data["interior"]),
            (sample_size, sample_size),
            contain=False,
            crop_anchor=str(data.get("interior_crop_anchor", "center")),
        )
    sample = ImageEnhance.Contrast(sample.convert("RGB")).enhance(1.05).convert("RGBA")
    sample.putalpha(rounded_mask(sample.size, sample_size // 2))
    sample_x = int(w * 0.59)
    sample_y = int(h * 0.405)
    paste_shadow(canvas, sample, (sample_x, sample_y), 18)
    draw.ellipse((sample_x - 6, sample_y - 6, sample_x + sample_size + 6, sample_y + sample_size + 6), outline=color, width=8)

    draw_centered_in(draw, str(data["line"]), (int(w * 0.56), int(h * 0.72), int(w * 0.98), int(h * 0.81)), font(int(w * 0.023), True), NAVY)
    draw.rounded_rectangle((int(w * 0.58), int(h * 0.82), int(w * 0.94), int(h * 0.875)), 30, fill=color)
    cta = "BUY ON AMAZON"
    cta_font = font(int(w * 0.024), True)
    cb = draw.textbbox((0, 0), cta, font=cta_font)
    draw.text((int(w * 0.76) - (cb[2] - cb[0]) // 2, int(h * 0.835)), cta, font=cta_font, fill=WHITE)
    draw.text((int(w * 0.59), int(h * 0.90)), "Ages 5–9  •  26 unique subjects", font=font(int(w * 0.020), True), fill=NAVY)
    draw.text((int(w * 0.59), int(h * 0.94)), "acornoodlebooks.com", font=font(int(w * 0.022), True), fill=RASPBERRY)
    return canvas


def inside_books(size: tuple[int, int]) -> Image.Image:
    w, h = size
    canvas = Image.new("RGBA", size, NAVY)
    draw = ImageDraw.Draw(canvas)
    for i, color in enumerate((GREEN, GOLD, SKY, RASPBERRY)):
        draw.ellipse((int(w * (0.04 + i * 0.25)), int(h * 0.04), int(w * (0.19 + i * 0.25)), int(h * 0.15)), fill=color)
    add_logo(canvas, int(h * 0.055), int(w * 0.44), panel=True)
    y = int(h * 0.19)
    y = draw_centered(draw, "BIG PICTURES.\nLITTLE FACTS.", y, font(int(w * 0.064), True), WHITE, w)
    draw_centered(draw, "Coloring adventures for growing hands and curious minds", y + 20, font(int(w * 0.025)), "#DCE9F5", w)

    card_w, card_h = int(w * 0.78), int(h * 0.43)
    card_x, card_y = (w - card_w) // 2, int(h * 0.40)
    draw.rounded_rectangle((card_x, card_y, card_x + card_w, card_y + card_h), 34, fill=WHITE)
    sample = fit_image(BOOKS["crawling-bugs"]["interior"], (int(card_w * 0.47), int(card_h * 0.72)), contain=True)
    canvas.alpha_composite(sample, (card_x + int(card_w * 0.04), card_y + int(card_h * 0.08)))
    tx = card_x + int(card_w * 0.53)
    ty = card_y + int(card_h * 0.12)
    features = [
        ("26", "unique subjects"),
        ("1", "real name + fact"),
        ("60", "generous pages"),
        ("1", "picture per page"),
    ]
    for number, label in features:
        draw.text((tx, ty), number, font=font(int(w * 0.044), True), fill=RASPBERRY)
        draw.text((tx + int(w * 0.075), ty + int(w * 0.01)), label, font=font(int(w * 0.024), True), fill=NAVY)
        ty += int(card_h * 0.20)
    draw_centered(draw, "COLOR. LEARN. DISCOVER.", int(h * 0.87), font(int(w * 0.030), True), GOLD, w)
    draw_centered(draw, "Explore all three books at acornoodlebooks.com", int(h * 0.92), font(int(w * 0.023), True), WHITE, w)
    return canvas


def save_all() -> None:
    for platform, size in FORMATS.items():
        target = OUT / platform
        target.mkdir(parents=True, exist_ok=True)
        launch_trio(size).convert("RGB").save(target / "01-launch-trio.jpg", quality=94, subsampling=0)
        for index, (slug, data) in enumerate(BOOKS.items(), 2):
            book_spotlight(size, data).convert("RGB").save(target / f"{index:02d}-{slug}.jpg", quality=94, subsampling=0)
        inside_books(size).convert("RGB").save(target / "05-inside-the-books.jpg", quality=94, subsampling=0)


if __name__ == "__main__":
    save_all()
    print(f"Built {len(FORMATS) * 5} launch assets in {OUT}")
