"""Generate PastureFrame icon set as transparent PNGs.

Renders a small set of pictogram icons used in the build manual at
`products/_shared/icons/`. All icons are 512x512 GREEN strokes on transparent.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[2] / "products" / "_shared" / "icons"
OUT.mkdir(parents=True, exist_ok=True)

GREEN = (31, 59, 36, 255)
RUST = (138, 75, 47, 255)
TAN = (200, 155, 97, 255)

SIZE = 512
STROKE = 22


def base() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def save(img: Image.Image, name: str) -> None:
    img.save(OUT / name, "PNG")
    print("wrote", name)


def line(d, p1, p2, color=GREEN, width=STROKE):
    d.line([p1, p2], fill=color, width=width)


def circle(d, c, r, color=GREEN, width=STROKE, fill=None):
    x, y = c
    d.ellipse([x - r, y - r, x + r, y + r], outline=color, width=width, fill=fill)


def rect(d, x1, y1, x2, y2, color=GREEN, width=STROKE, fill=None):
    d.rectangle([x1, y1, x2, y2], outline=color, width=width, fill=fill)


def poly(d, pts, color=GREEN, width=STROKE, fill=None):
    d.polygon(pts, outline=color, width=width, fill=fill)


# 1. Saw -------------------------------------------------------------------
def saw():
    img, d = base()
    # blade body
    rect(d, 90, 200, 380, 280, fill=TAN, color=GREEN)
    # teeth
    teeth_y = 280
    for x in range(100, 380, 30):
        poly(d, [(x, teeth_y), (x + 15, teeth_y + 35), (x + 30, teeth_y)],
             color=GREEN, fill=GREEN, width=2)
    # handle
    rect(d, 380, 170, 470, 310, fill=RUST, color=GREEN)
    line(d, (90, 230), (90, 280))
    save(img, "icon_saw.png")


# 2. Hammer ----------------------------------------------------------------
def hammer():
    img, d = base()
    # head
    poly(d, [(110, 110), (320, 110), (340, 230), (90, 230)], fill=GREEN, color=GREEN, width=2)
    # claw notch
    poly(d, [(110, 130), (180, 170), (110, 210)], fill=(247, 243, 232, 255), color=GREEN, width=2)
    # handle
    poly(d, [(180, 230), (250, 230), (310, 470), (240, 470)], fill=RUST, color=GREEN, width=2)
    save(img, "icon_hammer.png")


# 3. Drill -----------------------------------------------------------------
def drill():
    img, d = base()
    # body
    rect(d, 130, 170, 350, 290, fill=GREEN, color=GREEN, width=2)
    # chuck
    rect(d, 350, 200, 410, 260, fill=TAN, color=GREEN, width=2)
    # bit
    rect(d, 410, 220, 470, 240, fill=GREEN, color=GREEN, width=2)
    # handle
    poly(d, [(180, 290), (260, 290), (260, 460), (180, 460)], fill=RUST, color=GREEN, width=2)
    # trigger
    rect(d, 195, 290, 230, 320, fill=TAN, color=GREEN, width=2)
    save(img, "icon_drill.png")


# 4. Square ----------------------------------------------------------------
def square():
    img, d = base()
    poly(d, [(100, 100), (180, 100), (180, 350), (430, 350), (430, 430), (100, 430)],
         fill=TAN, color=GREEN, width=STROKE)
    # tick marks
    for x in range(200, 420, 30):
        line(d, (x, 350), (x, 380), color=GREEN, width=6)
    for y in range(120, 340, 30):
        line(d, (180, y), (210, y), color=GREEN, width=6)
    save(img, "icon_square.png")


# 5. Chicken (layer) -------------------------------------------------------
def chicken():
    img, d = base()
    # body
    d.ellipse([130, 200, 380, 430], fill=GREEN, outline=GREEN, width=2)
    # head
    d.ellipse([280, 130, 410, 260], fill=GREEN, outline=GREEN, width=2)
    # comb
    poly(d, [(310, 130), (330, 90), (350, 130), (370, 90), (390, 130)],
         fill=RUST, color=RUST, width=2)
    # beak
    poly(d, [(410, 200), (470, 220), (410, 240)], fill=TAN, color=TAN, width=2)
    # eye
    d.ellipse([350, 175, 380, 205], fill=(247, 243, 232, 255), outline=GREEN, width=4)
    # legs
    line(d, (220, 425), (220, 480), color=TAN, width=14)
    line(d, (300, 425), (300, 480), color=TAN, width=14)
    save(img, "icon_chicken.png")


# 6. Broiler --------------------------------------------------------------
def broiler():
    img, d = base()
    # plumper body
    d.ellipse([100, 220, 410, 450], fill=TAN, outline=GREEN, width=STROKE)
    # head
    d.ellipse([320, 150, 440, 270], fill=TAN, outline=GREEN, width=STROKE)
    # beak
    poly(d, [(440, 200), (490, 215), (440, 230)], fill=RUST, color=RUST, width=2)
    # eye
    d.ellipse([370, 180, 395, 205], fill=GREEN, outline=GREEN, width=2)
    # ground line
    line(d, (90, 470), (430, 470), color=GREEN, width=STROKE)
    save(img, "icon_broiler.png")


# 7. Snowflake ------------------------------------------------------------
def snowflake():
    img, d = base()
    cx, cy = 256, 256
    SKY = (74, 122, 140, 255)
    import math
    for k in range(6):
        a = math.radians(k * 60)
        x2 = cx + 200 * math.cos(a)
        y2 = cy + 200 * math.sin(a)
        line(d, (cx, cy), (x2, y2), color=SKY, width=STROKE)
        # branches
        for off in (-1, 1):
            ba = a + off * math.radians(35)
            bx = cx + 130 * math.cos(a) + 60 * math.cos(ba)
            by = cy + 130 * math.sin(a) + 60 * math.sin(ba)
            mx = cx + 130 * math.cos(a)
            my = cy + 130 * math.sin(a)
            line(d, (mx, my), (bx, by), color=SKY, width=STROKE - 4)
    circle(d, (cx, cy), 24, color=SKY, width=2, fill=SKY)
    save(img, "icon_snowflake.png")


# 8. Paw -------------------------------------------------------------------
def paw():
    img, d = base()
    CLAY = (184, 84, 64, 255)
    # main pad
    d.ellipse([180, 280, 360, 440], fill=CLAY, outline=CLAY, width=2)
    # toes
    for cx in (160, 240, 320, 400):
        cy = 200 if cx in (240, 320) else 250
        d.ellipse([cx - 35, cy - 40, cx + 35, cy + 40], fill=CLAY, outline=CLAY, width=2)
    save(img, "icon_paw.png")


# 9. Dollar ----------------------------------------------------------------
def dollar():
    img, d = base()
    SUN = (232, 178, 60, 255)
    circle(d, (256, 256), 200, color=SUN, width=STROKE, fill=(247, 243, 232, 255))
    # big $
    try:
        from PIL import ImageFont
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 260)
        bbox = d.textbbox((0, 0), "$", font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        d.text(((SIZE - w) / 2 - bbox[0], (SIZE - h) / 2 - bbox[1] - 10),
               "$", font=font, fill=SUN)
    except Exception:
        d.text((215, 145), "$", fill=SUN)
    save(img, "icon_dollar.png")


# 10. Calendar -------------------------------------------------------------
def calendar():
    img, d = base()
    # body
    rect(d, 90, 130, 420, 440, fill=(247, 243, 232, 255), color=GREEN)
    # top band
    rect(d, 90, 130, 420, 200, fill=GREEN, color=GREEN, width=2)
    # rings
    rect(d, 140, 100, 175, 175, fill=RUST, color=RUST, width=2)
    rect(d, 335, 100, 370, 175, fill=RUST, color=RUST, width=2)
    # grid
    for x in range(150, 410, 65):
        line(d, (x, 220), (x, 430), color=GREEN, width=6)
    for y in range(220, 430, 50):
        line(d, (100, y), (410, y), color=GREEN, width=6)
    save(img, "icon_calendar.png")


# 11. Check ----------------------------------------------------------------
def check():
    img, d = base()
    rect(d, 100, 100, 412, 412, fill=GREEN, color=GREEN)
    # tick
    line(d, (160, 270), (240, 350), color=(247, 243, 232, 255), width=42)
    line(d, (240, 350), (370, 180), color=(247, 243, 232, 255), width=42)
    save(img, "icon_check.png")


# 12. App / phone ---------------------------------------------------------
def app():
    img, d = base()
    rect(d, 160, 80, 360, 460, fill=GREEN, color=GREEN)
    rect(d, 180, 130, 340, 410, fill=(247, 243, 232, 255), color=(247, 243, 232, 255))
    # speaker dot
    circle(d, (260, 105), 10, color=TAN, fill=TAN, width=2)
    # screen content - 3 rows
    for i, y in enumerate([180, 250, 320]):
        rect(d, 200, y, 320, y + 40, fill=TAN if i == 0 else (247, 243, 232, 255), color=GREEN, width=4)
    # home button
    circle(d, (260, 435), 18, color=TAN, fill=TAN, width=2)
    save(img, "icon_app.png")


# 13. Signature ------------------------------------------------------------
def signature():
    img, d = base()
    # paper
    rect(d, 90, 140, 420, 410, fill=(247, 243, 232, 255), color=GREEN)
    # ruled lines
    for y in (220, 280, 340):
        line(d, (120, y), (390, y), color=GREEN, width=6)
    # cursive squiggle as signature
    pts = [(140, 330), (180, 290), (220, 340), (260, 290), (300, 350), (340, 290), (380, 320)]
    for a, b in zip(pts, pts[1:]):
        line(d, a, b, color=RUST, width=10)
    save(img, "icon_signature.png")


def main():
    saw()
    hammer()
    drill()
    square()
    chicken()
    broiler()
    snowflake()
    paw()
    dollar()
    calendar()
    check()
    app()
    signature()
    print("all icons in", OUT)


if __name__ == "__main__":
    main()
