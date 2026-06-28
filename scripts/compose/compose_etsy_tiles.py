"""Compose 10 Etsy listing tiles (2000x2000) from existing assets.

Output: products/mobile-chicken-coop-10x10/deliverables/etsy_listing_images/01..10_*.png
No new artwork is generated; only existing PNGs are arranged + overlaid with
PastureFrame brand text.
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
PRODUCT = ROOT / "products" / "mobile-chicken-coop-10x10"
DRAW = PRODUCT / "final_plan_package" / "drawing_assets" / "png"
STEPS = PRODUCT / "source" / "images" / "readable_step_cards"
INFO = PRODUCT / "final_plan_package" / "current_plan_assets" / "original_chicken_coop_infographic.png"
CONTACT = PRODUCT / "final_plan_package" / "current_plan_assets" / "mobile_chicken_coop_plan_set_contact_sheet.png"
OUT = PRODUCT / "deliverables" / "etsy_listing_images"
OUT.mkdir(parents=True, exist_ok=True)

SIZE = 2000
GREEN = (31, 59, 36)
TAN = (200, 155, 97)
CREAM = (247, 243, 232)
CHAR = (37, 37, 37)
RUST = (138, 75, 47)
GRAY = (125, 129, 120)
WHITE = (255, 255, 255)

FONTS = "/System/Library/Fonts/Supplemental"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(f"{FONTS}/{name}", size)


def fit(img: Image.Image, w: int, h: int, bg=CREAM) -> Image.Image:
    """Resize image to fit within w x h, padded on cream background."""
    src = img.copy()
    src.thumbnail((w, h), Image.LANCZOS)
    canvas = Image.new("RGB", (w, h), bg)
    canvas.paste(src, ((w - src.width) // 2, (h - src.height) // 2))
    return canvas


def text_center(d: ImageDraw.ImageDraw, xy, text, fnt, fill):
    bbox = d.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    cx, cy = xy
    d.text((cx - tw / 2, cy - th / 2 - bbox[1]), text, font=fnt, fill=fill)


def text_left(d: ImageDraw.ImageDraw, xy, text, fnt, fill):
    bbox = d.textbbox((0, 0), text, font=fnt)
    d.text((xy[0], xy[1] - bbox[1]), text, font=fnt, fill=fill)


def base_canvas(bg=CREAM) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGB", (SIZE, SIZE), bg)
    return im, ImageDraw.Draw(im)


def banner(d: ImageDraw.ImageDraw, y: int, h: int, text: str, fnt, color=GREEN, fg=WHITE):
    d.rectangle([0, y, SIZE, y + h], fill=color)
    text_center(d, (SIZE // 2, y + h // 2), text, fnt, fg)


def footer(d: ImageDraw.ImageDraw, label="PastureFrame Plans  ·  Designed by Ashton Aschenbrener"):
    fnt = font("Arial.ttf", 36)
    d.rectangle([0, SIZE - 80, SIZE, SIZE], fill=GREEN)
    text_center(d, (SIZE // 2, SIZE - 40), label, fnt, CREAM)


# --------------------------------------------------------------------------- #
# Tile 1 — Hero
# --------------------------------------------------------------------------- #
def tile_01_hero():
    im, d = base_canvas(CREAM)
    src = Image.open(INFO).convert("RGB")
    inner = fit(src, 1820, 1100)
    im.paste(inner, ((SIZE - 1820) // 2, 360))

    banner(d, 0, 280, "10x10 MOBILE CHICKEN COOP", font("Impact.ttf", 180))
    text_center(d, (SIZE // 2, 320), "with 4x10 ELEVATED COOP HOUSE", font("Arial Bold.ttf", 72), GREEN)

    # bottom call-out band
    d.rectangle([0, 1500, SIZE, 1820], fill=RUST)
    text_center(d, (SIZE // 2, 1580), "DIGITAL DIY PLANS — PDF DOWNLOAD", font("Arial Black.ttf", 96), CREAM)
    text_center(d, (SIZE // 2, 1700), "NO PHYSICAL COOP SHIPPED", font("Arial Bold.ttf", 78), CREAM)

    footer(d)
    im.save(OUT / "01_hero.png", "PNG")


# --------------------------------------------------------------------------- #
# Tile 2 — Dimensions
# --------------------------------------------------------------------------- #
def tile_02_dimensions():
    im, d = base_canvas(CREAM)
    banner(d, 0, 230, "CONFIRMED DIMENSIONS", font("Impact.ttf", 150))

    side = Image.open(DRAW / "side_elevation_48in_run.png").convert("RGB")
    panel = fit(side, 1820, 1000)
    im.paste(panel, ((SIZE - 1820) // 2, 280))

    rows = [
        ("Outside footprint", "10' x 10'"),
        ("Lower run height", "48\" (mobile)"),
        ("Elevated coop", "4' x 10' over rear 48\""),
        ("Upper walls", "48\" high / 40\" low"),
        ("Roof fall", "approx. 8\" across 48\""),
    ]
    y = 1340
    fnt_l = font("Georgia Bold.ttf", 56)
    fnt_r = font("Arial Bold.ttf", 56)
    for label, value in rows:
        d.rectangle([100, y, SIZE - 100, y + 80], outline=GREEN, width=4)
        text_left(d, (140, y + 40), label, fnt_l, GREEN)
        text_left(d, (1150, y + 40), value, fnt_r, RUST)
        y += 100

    footer(d)
    im.save(OUT / "02_dimensions.png", "PNG")


# --------------------------------------------------------------------------- #
# Tile 3 — Top View
# --------------------------------------------------------------------------- #
def tile_03_top_view():
    im, d = base_canvas(CREAM)
    banner(d, 0, 230, "TOP-DOWN PLAN VIEW", font("Impact.ttf", 150))
    src = Image.open(DRAW / "dimensioned_top_view.png").convert("RGB")
    panel = fit(src, 1820, 1450)
    im.paste(panel, ((SIZE - 1820) // 2, 270))

    text_center(d, (SIZE // 2, 1830), "Run + elevated coop layout · nest/roost zone · access points",
                font("Georgia Italic.ttf", 54), CHAR)
    footer(d)
    im.save(OUT / "03_top_view.png", "PNG")


# --------------------------------------------------------------------------- #
# Tile 4 — Side Elevation
# --------------------------------------------------------------------------- #
def tile_04_side_elevation():
    im, d = base_canvas(CREAM)
    banner(d, 0, 230, "SIDE ELEVATION · 48\" MOBILE RUN", font("Impact.ttf", 130))
    src = Image.open(DRAW / "side_elevation_48in_run.png").convert("RGB")
    panel = fit(src, 1820, 1450)
    im.paste(panel, ((SIZE - 1820) // 2, 270))
    text_center(d, (SIZE // 2, 1830), "Sloped roof · pop door · ramp · skids and tow tongue",
                font("Georgia Italic.ttf", 54), CHAR)
    footer(d)
    im.save(OUT / "04_side_elevation.png", "PNG")


# --------------------------------------------------------------------------- #
# Tile 5 — Exploded Frame
# --------------------------------------------------------------------------- #
def tile_05_exploded():
    im, d = base_canvas(CREAM)
    banner(d, 0, 230, "EXPLODED FRAME SCHEMATIC", font("Impact.ttf", 140))
    src = Image.open(DRAW / "exploded_frame_schematic.png").convert("RGB")
    panel = fit(src, 1820, 1450)
    im.paste(panel, ((SIZE - 1820) // 2, 270))
    text_center(d, (SIZE // 2, 1830), "Skids · base frame · 9 posts · upper coop · roof",
                font("Georgia Italic.ttf", 54), CHAR)
    footer(d)
    im.save(OUT / "05_exploded.png", "PNG")


# --------------------------------------------------------------------------- #
# Tile 6 — Wheel / Skid / Tow
# --------------------------------------------------------------------------- #
def tile_06_wheel_skid():
    im, d = base_canvas(CREAM)
    banner(d, 0, 230, "WHEEL · SKID · TOW DETAIL", font("Impact.ttf", 140))
    src = Image.open(DRAW / "wheel_skid_tow_tongue_detail.png").convert("RGB")
    panel = fit(src, 1820, 1300)
    im.paste(panel, ((SIZE - 1820) // 2, 270))

    bullets = [
        "4x6 PT skids, 10 ft, beveled tow ends",
        "20\" pneumatic wheels, 600 lb+ rating each",
        "3/4\" axle rod or hub/spindle assemblies",
        "4x4 or steel tow tongue + ring + safety chain",
    ]
    fnt = font("Arial Bold.ttf", 48)
    y = 1640
    for b in bullets:
        d.rectangle([200, y, 240, y + 40], fill=RUST)
        text_left(d, (280, y + 20), b, fnt, CHAR)
        y += 60
    footer(d)
    im.save(OUT / "06_wheel_skid.png", "PNG")


# --------------------------------------------------------------------------- #
# Tile 7 — Layer setup
# --------------------------------------------------------------------------- #
def tile_07_layers():
    im, d = base_canvas(CREAM)
    banner(d, 0, 230, "LAYER SETUP · 10–12 HENS", font("Impact.ttf", 140))

    nest = Image.open(DRAW / "nest_roost_layout.png").convert("RGB")
    layer_card = Image.open(STEPS / "step_13_layer_setup.png").convert("RGB")
    left = fit(nest, 940, 1300)
    right = fit(layer_card, 840, 1300)
    im.paste(left, (60, 280))
    im.paste(right, (60 + 940 + 40, 280))

    bullets = [
        "3 nest boxes · 12W x 12H x 14D",
        "10–12 ft removable roost bars",
        "Pop door + cleanout + nest hatch",
    ]
    fnt = font("Arial Bold.ttf", 50)
    y = 1620
    for b in bullets:
        d.rectangle([200, y, 240, y + 40], fill=GREEN)
        text_left(d, (280, y + 20), b, fnt, CHAR)
        y += 70
    footer(d)
    im.save(OUT / "07_layer_setup.png", "PNG")


# --------------------------------------------------------------------------- #
# Tile 8 — Broiler setup
# --------------------------------------------------------------------------- #
def tile_08_broilers():
    im, d = base_canvas(CREAM)
    banner(d, 0, 230, "BROILER SETUP · 30–45 BIRDS", font("Impact.ttf", 140))
    card = Image.open(STEPS / "step_12_broiler_setup.png").convert("RGB")
    panel = fit(card, 1820, 1280)
    im.paste(panel, ((SIZE - 1820) // 2, 270))

    bullets = [
        "Open lower run · ground access",
        "Roosts removed · feeders + waterers",
        "Frequent moves · shade + heat plan",
        "Up to ~50 only with strict management",
    ]
    fnt = font("Arial Bold.ttf", 48)
    y = 1610
    for b in bullets:
        d.rectangle([200, y, 240, y + 40], fill=RUST)
        text_left(d, (280, y + 20), b, fnt, CHAR)
        y += 60
    footer(d)
    im.save(OUT / "08_broiler_setup.png", "PNG")


# --------------------------------------------------------------------------- #
# Tile 9 — What's included
# --------------------------------------------------------------------------- #
def tile_09_whats_included():
    im, d = base_canvas(CREAM)
    banner(d, 0, 230, "WHAT'S INCLUDED", font("Impact.ttf", 170))

    items = [
        ("MAIN PDF PLAN", "Multi-page · dimensioned · exploded views"),
        ("MATERIALS LIST", "Strict v2 quantities + acceptance checks"),
        ("CUT LIST", "Board-by-board · 28 cut rows"),
        ("15 BUILD STEPS", "Base → Posts → Walls → Roof → Wheels"),
        ("DIMENSIONED DRAWINGS", "Top · side · exploded · wheel · nest"),
        ("LAYER + BROILER NOTES", "Nest, roost, capacity, movement"),
        ("SAFETY + DISCLAIMER", "DIY use · verify locally before building"),
    ]
    fnt_t = font("Arial Black.ttf", 60)
    fnt_b = font("Georgia Italic.ttf", 44)
    y = 320
    for title, sub in items:
        d.rectangle([100, y, SIZE - 100, y + 180], outline=GREEN, width=5)
        d.rectangle([100, y, 130, y + 180], fill=RUST)
        text_left(d, (170, y + 50), title, fnt_t, GREEN)
        text_left(d, (170, y + 130), sub, fnt_b, CHAR)
        y += 200
    footer(d)
    im.save(OUT / "09_whats_included.png", "PNG")


# --------------------------------------------------------------------------- #
# Tile 10 — Disclaimer
# --------------------------------------------------------------------------- #
def tile_10_disclaimer():
    im, d = base_canvas(GREEN)
    text_center(d, (SIZE // 2, 220), "PLEASE READ", font("Impact.ttf", 180), CREAM)
    text_center(d, (SIZE // 2, 360), "BEFORE PURCHASE", font("Arial Bold.ttf", 100), TAN)

    body_lines = [
        "This is a DIGITAL DOWNLOAD.",
        "No physical coop is shipped.",
        "",
        "Plans are provided for general DIY",
        "educational use. Site conditions, codes,",
        "wind/snow load, and predator pressure vary.",
        "",
        "Verify dimensions, materials, and safety",
        "for your location BEFORE building.",
        "",
        "Not engineered, not code-approved,",
        "not field-tested, not predator-proof.",
        "",
        "Personal use only · No resale.",
    ]
    fnt = font("Georgia.ttf", 56)
    y = 520
    for line in body_lines:
        text_center(d, (SIZE // 2, y), line, fnt, CREAM)
        y += 80

    d.rectangle([0, SIZE - 130, SIZE, SIZE], fill=CREAM)
    text_center(d, (SIZE // 2, SIZE - 65),
                "PastureFrame Plans  ·  Designed by Ashton Aschenbrener",
                font("Arial Bold.ttf", 42), GREEN)
    im.save(OUT / "10_disclaimer.png", "PNG")


def main():
    tile_01_hero()
    tile_02_dimensions()
    tile_03_top_view()
    tile_04_side_elevation()
    tile_05_exploded()
    tile_06_wheel_skid()
    tile_07_layers()
    tile_08_broilers()
    tile_09_whats_included()
    tile_10_disclaimer()
    print("Wrote 10 tiles to", OUT)


if __name__ == "__main__":
    main()
