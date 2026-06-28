"""Compose buyer-facing PDF manual from existing assets + strict v2 spec text.

Uses reportlab platypus. Output:
products/mobile-chicken-coop-10x10/deliverables/pdf/PastureFrame_Mobile_Coop_10x10_Plans_v1.0.0.pdf
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image as RLImage,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[2]
PRODUCT = ROOT / "products" / "mobile-chicken-coop-10x10"
DRAW = PRODUCT / "final_plan_package" / "drawing_assets" / "png"
STEPS = PRODUCT / "source" / "images" / "readable_step_cards"
INFO = PRODUCT / "final_plan_package" / "current_plan_assets" / "original_chicken_coop_infographic.png"
OUT_DIR = PRODUCT / "deliverables" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT = OUT_DIR / "PastureFrame_Mobile_Coop_10x10_Plans_v2.0.0.pdf"
APP_URL = "https://pastureframe-coop-build-companion.vercel.app/"
PRODUCT_VERSION = "2.0.0"
ICONS = ROOT / "products" / "_shared" / "icons"

# Brand
GREEN = colors.HexColor("#1F3B24")
TAN = colors.HexColor("#C89B61")
CREAM = colors.HexColor("#F7F3E8")
CHAR = colors.HexColor("#252525")
RUST = colors.HexColor("#8A4B2F")
GRAY = colors.HexColor("#7D8178")
# Expanded accents (sparingly)
SUN = colors.HexColor("#E8B23C")
SKY = colors.HexColor("#4A7A8C")
CLAY = colors.HexColor("#B85440")
MOSS = colors.HexColor("#6E8C58")

# Fonts
SYS = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("PF-Sans", f"{SYS}/Arial.ttf"))
pdfmetrics.registerFont(TTFont("PF-SansBold", f"{SYS}/Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("PF-Serif", f"{SYS}/Georgia.ttf"))
pdfmetrics.registerFont(TTFont("PF-SerifBold", f"{SYS}/Georgia Bold.ttf"))
pdfmetrics.registerFont(TTFont("PF-SerifItalic", f"{SYS}/Georgia Italic.ttf"))
pdfmetrics.registerFont(TTFont("PF-Display", f"{SYS}/Impact.ttf"))

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="PF-Display", fontSize=30, leading=36, textColor=GREEN, spaceAfter=4)
H1_SUB = ParagraphStyle("H1S", parent=styles["BodyText"], fontName="PF-SerifItalic", fontSize=14, leading=20, textColor=RUST, spaceAfter=14)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="PF-SansBold", fontSize=16, leading=22, textColor=GREEN, spaceAfter=8, spaceBefore=14)
H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="PF-SansBold", fontSize=13, leading=18, textColor=RUST, spaceAfter=4, spaceBefore=10)
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontName="PF-Serif", fontSize=12, leading=17, textColor=CHAR, spaceAfter=8)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=10, leading=13, textColor=GRAY)
CAPTION = ParagraphStyle("Caption", parent=BODY, fontName="PF-SerifItalic", fontSize=10.5, leading=14, alignment=1, textColor=GRAY)
COVER_TITLE = ParagraphStyle("CT", fontName="PF-Display", fontSize=64, leading=72, textColor=CREAM, alignment=1)
COVER_SUB = ParagraphStyle("CS", fontName="PF-SansBold", fontSize=24, leading=30, textColor=TAN, alignment=1)
COVER_LINE = ParagraphStyle("CL", fontName="PF-Serif", fontSize=15, leading=22, textColor=CREAM, alignment=1)
LIST_BODY = ParagraphStyle("LB", parent=BODY, leftIndent=18, bulletIndent=4, spaceAfter=4)
DIV_NUM = ParagraphStyle("DN", fontName="PF-Display", fontSize=42, leading=50, textColor=TAN, alignment=1)
DIV_TITLE = ParagraphStyle("DT", fontName="PF-Display", fontSize=56, leading=64, textColor=GREEN, alignment=1)
DIV_SUB = ParagraphStyle("DS", fontName="PF-SerifItalic", fontSize=18, leading=24, textColor=RUST, alignment=1)
CALLOUT_BODY = ParagraphStyle("COB", parent=BODY, fontSize=11, leading=15, spaceAfter=2)

PAGE_W, PAGE_H = LETTER
MARGIN_X = 0.7 * inch
MARGIN_TOP = 0.85 * inch
MARGIN_BOT = 0.85 * inch


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(GREEN)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # Tan band
    canvas.setFillColor(TAN)
    canvas.rect(0, PAGE_H - 1.6 * inch, PAGE_W, 0.2 * inch, stroke=0, fill=1)
    canvas.rect(0, 1.4 * inch, PAGE_W, 0.2 * inch, stroke=0, fill=1)
    canvas.restoreState()


def divider_page_bg(canvas, doc):
    """Full-bleed CREAM with GREEN top bar + TAN bottom bar."""
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas.setFillColor(GREEN)
    canvas.rect(0, PAGE_H - 1.3 * inch, PAGE_W, 1.3 * inch, stroke=0, fill=1)
    canvas.setFillColor(TAN)
    canvas.rect(0, 0, PAGE_W, 1.3 * inch, stroke=0, fill=1)
    canvas.restoreState()


def content_header_footer(canvas, doc):
    canvas.saveState()
    # Header band - taller, more breathing room
    canvas.setFillColor(GREEN)
    canvas.rect(0, PAGE_H - 0.55 * inch, PAGE_W, 0.55 * inch, stroke=0, fill=1)
    canvas.setFillColor(CREAM)
    canvas.setFont("PF-SansBold", 12)
    canvas.drawString(MARGIN_X, PAGE_H - 0.36 * inch, "PASTUREFRAME PLANS")
    canvas.setFont("PF-Sans", 10)
    canvas.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 0.36 * inch,
                           f"10' x 10' Mobile Chicken Coop · v{PRODUCT_VERSION}")
    # Footer band
    canvas.setFillColor(GREEN)
    canvas.rect(0, 0, PAGE_W, 0.45 * inch, stroke=0, fill=1)
    canvas.setFillColor(CREAM)
    canvas.setFont("PF-Sans", 9)
    canvas.drawString(MARGIN_X, 0.18 * inch,
                      f"© {date.today().year} PastureFrame Plans · Designed by Ashton Aschenbrener · Personal use only")
    canvas.drawRightString(PAGE_W - MARGIN_X, 0.18 * inch, f"Page {doc.page}")
    canvas.restoreState()


def make_doc(path: Path) -> BaseDocTemplate:
    doc = BaseDocTemplate(
        str(path),
        pagesize=LETTER,
        leftMargin=MARGIN_X,
        rightMargin=MARGIN_X,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOT,
        title="PastureFrame 10x10 Mobile Chicken Coop Plans",
        author="Ashton Aschenbrener",
        subject="DIY mobile chicken coop digital plans",
    )
    cover_frame = Frame(0.8 * inch, 0.8 * inch, PAGE_W - 1.6 * inch, PAGE_H - 1.6 * inch, id="cover")
    body_frame = Frame(MARGIN_X, MARGIN_BOT, PAGE_W - 2 * MARGIN_X,
                       PAGE_H - MARGIN_TOP - MARGIN_BOT - 0.2 * inch, id="body")
    div_frame = Frame(0.8 * inch, 1.6 * inch, PAGE_W - 1.6 * inch,
                      PAGE_H - 3.2 * inch, id="divider")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=cover_page),
        PageTemplate(id="body", frames=[body_frame], onPage=content_header_footer),
        PageTemplate(id="divider", frames=[div_frame], onPage=divider_page_bg),
    ])
    return doc


def fitted_image(path: Path, max_w: float, max_h: float) -> RLImage:
    img = RLImage(str(path))
    iw, ih = img.imageWidth, img.imageHeight
    scale = min(max_w / iw, max_h / ih)
    img.drawWidth = iw * scale
    img.drawHeight = ih * scale
    return img


def icon_image(name: str, size_in: float = 0.5) -> RLImage | None:
    """Return an RLImage for the icon if it exists, else None."""
    p = ICONS / f"icon_{name}.png"
    if not p.exists():
        return None
    img = RLImage(str(p))
    img.drawWidth = size_in * inch
    img.drawHeight = size_in * inch
    return img


def chapter_h1(num: int, title: str, subtitle: str | None = None,
               icon_name: str | None = None) -> list:
    """Render an H1 row + optional icon + decorative italic subtitle."""
    flow = []
    if icon_name:
        ico = icon_image(icon_name, 0.55)
        if ico is not None:
            cells = [[ico, Paragraph(f"{num} &middot; {title.upper()}", H1)]]
            t = Table(cells, colWidths=[0.7 * inch, None])
            t.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))
            flow.append(t)
        else:
            flow.append(Paragraph(f"{num} &middot; {title.upper()}", H1))
    else:
        flow.append(Paragraph(f"{num} &middot; {title.upper()}", H1))
    if subtitle:
        flow.append(Paragraph(subtitle, H1_SUB))
    return flow


def divider_page(part_num: str, title: str, subtitle: str,
                 icon_name: str | None = None) -> list:
    """Build a section divider page sequence (returns list of flowables ending in PageBreak)."""
    flow = [NextPageTemplate("divider"), PageBreak()]
    flow.append(Spacer(1, 0.6 * inch))
    flow.append(Paragraph(part_num.upper(), DIV_NUM))
    flow.append(Spacer(1, 0.15 * inch))
    flow.append(Paragraph(title.upper(), DIV_TITLE))
    flow.append(Spacer(1, 0.15 * inch))
    flow.append(Paragraph(subtitle, DIV_SUB))
    if icon_name:
        ico = icon_image(icon_name, 1.5)
        if ico is not None:
            flow.append(Spacer(1, 0.4 * inch))
            ico.hAlign = "CENTER"
            flow.append(ico)
    flow.append(NextPageTemplate("body"))
    flow.append(PageBreak())
    return flow


CALLOUT_THEMES = {
    "tip":     {"label": "PRO TIP",         "bar": SUN,   "label_fg": CHAR},
    "mistake": {"label": "COMMON MISTAKE",  "bar": CLAY,  "label_fg": CREAM},
    "safety":  {"label": "SAFETY",          "bar": GREEN, "label_fg": CREAM},
    "winter":  {"label": "WINTER NOTE",     "bar": SKY,   "label_fg": CREAM},
    "money":   {"label": "MONEY MOVE",      "bar": MOSS,  "label_fg": CREAM},
}


def callout(kind: str, body_text: str, label_override: str | None = None) -> Table:
    theme = CALLOUT_THEMES[kind]
    label = label_override or theme["label"]
    label_style = ParagraphStyle("col", fontName="PF-SansBold", fontSize=12,
                                 leading=15, textColor=theme["label_fg"])
    body_style = ParagraphStyle("cob", parent=CALLOUT_BODY)
    rows = [[Paragraph(label, label_style)],
            [Paragraph(body_text, body_style)]]
    t = Table(rows, colWidths=[PAGE_W - 2 * MARGIN_X - 0.05 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), theme["bar"]),
        ("BACKGROUND", (0, 1), (-1, 1), CREAM),
        ("BOX", (0, 0), (-1, -1), 0.5, theme["bar"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (0, 0), 6),
        ("BOTTOMPADDING", (0, 0), (0, 0), 6),
        ("TOPPADDING", (0, 1), (0, 1), 10),
        ("BOTTOMPADDING", (0, 1), (0, 1), 12),
    ]))
    return t


def step_card(step_num: str, title: str, subtitle: str,
              image_path: Path, bullets: list[str]) -> list:
    flow = []
    flow.append(Paragraph(f"STEP {step_num} &middot; {title.upper()}", H1))
    flow.append(Paragraph(subtitle, H1_SUB))
    # framed image
    img = fitted_image(image_path, 6.5 * inch, 4.6 * inch)
    img.hAlign = "CENTER"
    frame_tbl = Table([[img]], colWidths=[None])
    frame_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("BOX", (0, 0), (-1, -1), 1.2, RUST),
        ("INNERGRID", (0, 0), (-1, -1), 0, CREAM),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    flow.append(frame_tbl)
    flow.append(Spacer(1, 0.12 * inch))
    # acceptance badge
    badge = Table([[Paragraph(
        '<font color="#F7F3E8" name="PF-SansBold" size="11">ACCEPTANCE CHECKLIST</font>',
        ParagraphStyle("bg", alignment=0))]],
        colWidths=[PAGE_W - 2 * MARGIN_X])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GREEN),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    flow.append(badge)
    flow.append(Spacer(1, 0.08 * inch))
    for b in bullets:
        flow.append(Paragraph(f'<font color="#8A4B2F" size="14">&#9744;</font> &nbsp;{b}', LIST_BODY))
    return flow


def materials_table() -> Table:
    cell = ParagraphStyle("mc", fontName="PF-Sans", fontSize=9, leading=11, textColor=CHAR)
    cellb = ParagraphStyle("mcb", fontName="PF-SansBold", fontSize=9, leading=11, textColor=GREEN)
    head = ParagraphStyle("mch", fontName="PF-SansBold", fontSize=9.5, leading=12, textColor=CREAM)
    def P(text, style=cell):
        return Paragraph(text.replace("\"", "&quot;"), style)
    raw = [
        ["Category", "Item", "Qty", "Spec / acceptance check"],
        ["Ground/contact", "4x6 PT skids, 10 ft", "2", "Bevel tow/front ends; keep skids parallel."],
        ["Ground/contact", "2x6 PT lumber, 10 ft", "8–10", "Base perimeter, cross ties, upper coop floor rims."],
        ["Posts", "4x4 PT posts, 8 ft", "9", "3 front, 3 coop-front, 3 rear. Cut to plan heights."],
        ["Framing", "2x4 exterior/treated, 8 ft", "32–40", "Run rails, walls, braces, rafters, doors, ramp."],
        ["Roof", "1x4 or 2x4 purlins, 12 ft", "4", "Run side-to-side under corrugated roofing."],
        ["Sheet goods", "3/4\" exterior plywood, 4x8", "2", "Upper coop floor."],
        ["Sheet goods", "1/2\" plywood or T1-11, 4x8", "5", "Walls, doors, shutters, nest hatch, trim."],
        ["Wire", "1/2\" 19-ga galv. HW cloth (48\"×100')", "1 roll", "Walls, vents, windows; optional apron."],
        ["Roofing", "Corrugated panels ~36\" x 72\"", "4", "Metal/poly/bitumen; overlap per maker."],
        ["Mobility", "20\" pneumatic wheels, 600 lb+", "2", "Higher rating for rough ground."],
        ["Mobility", "3/4\" axle rod or hub/spindle", "1 set", "Washers, collars, cotter pins, through-bolts."],
        ["Mobility", "Tow tongue + ring + safety chain", "1 set", "Tow w/ ATV, UTV, or compact tractor."],
        ["Fasteners", "3\" exterior structural screws", "2 boxes", "Framing connections; predrill near ends."],
        ["Fasteners", "1-5/8\" exterior screws", "1 box", "Plywood and siding."],
        ["Fasteners", "1-1/4\" lath screws + fender washers", "1 box ea", "Hardware cloth attachment."],
        ["Fasteners", "5/16–3/8\" galv bolts/washers/locknuts", "Assorted", "Wheel mounts, tongue, heavy hinges."],
        ["Hardware", "Heavy strap hinges", "8–12", "Doors, cleanout panels, nest hatch."],
        ["Hardware", "Predator-resistant latches", "8–10", "Two-step latches on exterior doors."],
        ["Interior", "Nest boxes, roost bars, feeders", "As&nbsp;needed", "Layer mode uses nests/roosts."],
        ["Finish", "Exterior paint/stain, caulk, drip edge", "As needed", "Seal cut ends and roof penetrations."],
    ]
    rows = [[P(raw[0][0], head), P(raw[0][1], head), P(raw[0][2], head), P(raw[0][3], head)]]
    for r in raw[1:]:
        rows.append([P(r[0], cellb), P(r[1]), P(r[2]), P(r[3])])
    t = Table(rows, colWidths=[1.15 * inch, 2.0 * inch, 0.85 * inch, 3.2 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.25, GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def cut_table() -> Table:
    cell = ParagraphStyle("cc", fontName="PF-Sans", fontSize=8.5, leading=11, textColor=CHAR)
    cellb = ParagraphStyle("ccb", fontName="PF-SansBold", fontSize=8.5, leading=11, textColor=GREEN)
    head = ParagraphStyle("cch", fontName="PF-SansBold", fontSize=9, leading=11, textColor=CREAM)
    def P(text, style=cell):
        return Paragraph(text.replace("\"", "&quot;"), style)
    raw = [
        ["Section", "Part", "Material", "Qty", "Cut", "Notes"],
        ["Skids", "Left/right skids", "4x6 PT", "2", "120\"", "Bevel tow ends."],
        ["Base", "Long side perimeter rails", "2x6 PT", "2", "120\"", "Outside base length."],
        ["Base", "Front/rear perimeter rails", "2x6 PT", "2", "117\"", "Fit between long rails."],
        ["Base", "Base cross ties", "2x6 PT", "3", "117\"", "Near 48, 72, 96\" from front."],
        ["Posts", "Front lower-run posts", "4x4 PT", "3", "48\"", "Front L/C/R."],
        ["Posts", "Coop-front/high posts", "4x4 PT", "3", "96\"", "48\" run + 48\" wall."],
        ["Posts", "Rear/low posts", "4x4 PT", "3", "88\"", "48\" run + 40\" wall."],
        ["Lower run", "Side top/bottom rails", "2x4", "8", "Field", "Between post lines; keep square."],
        ["Lower run", "Front access door stiles", "2x4", "2", "42\"", "Hardware-cloth infill."],
        ["Lower run", "Front access door rails", "2x4", "2", "30\"", "Two-step latch."],
        ["Lower run", "Diagonal braces", "2x4", "8", "Field", "Install before moving frame."],
        ["Coop floor", "Front/rear floor rims", "2x6", "2", "120\"", "4'x10' floor frame."],
        ["Coop floor", "End rims and joists", "2x6", "9", "45\"", "~16\" O.C."],
        ["Coop floor", "Floor plywood main", "3/4\" ply", "1", "48x96\"", "Support all edges."],
        ["Coop floor", "Floor plywood filler", "3/4\" ply", "1", "48x24\"", "Complete 4'x10'."],
        ["Coop walls", "Front wall plates", "2x4", "2", "120\"", "High side."],
        ["Coop walls", "Front wall studs", "2x4", "7", "45\"", "Adjust for openings."],
        ["Coop walls", "Rear wall plates", "2x4", "2", "120\"", "Low side."],
        ["Coop walls", "Rear wall studs", "2x4", "7", "37\"", "Adjust for openings."],
        ["Coop walls", "End wall framing", "2x4", "Asst", "Field", "Slope 48→40\"."],
        ["Roof", "Rafters", "2x4", "7", "60\"", "Front-to-back w/ overhang."],
        ["Roof", "Purlins", "1x4/2x4", "4", "132\"", "Side-to-side."],
        ["Roof", "Roof panels", "Corrugated", "4", "72\"", "Overlap per maker."],
        ["Doors", "Rear cleanout door frames", "2x4", "2 sets", "Field", "~54x34\" each."],
        ["Doors", "Pop door", "1/2\" ply", "1", "12x14\"", "Predator latch."],
        ["Ramp", "Ramp deck", "1/2\" ply", "1", "14x60\"", "Cleats every 6\"."],
        ["Nest boxes", "Nest dividers/fronts", "1/2\" ply", "3 boxes", "Field", "12W x 12H x 14D each."],
        ["Roosts", "Removable roost bars", "2x3/2x4", "2", "60–72\"", "10–12 lf for 10–12 hens."],
    ]
    rows = [[P(c, head) for c in raw[0]]]
    for r in raw[1:]:
        rows.append([P(r[0], cellb)] + [P(c) for c in r[1:]])
    t = Table(rows, colWidths=[0.95 * inch, 1.9 * inch, 0.85 * inch, 0.6 * inch, 0.85 * inch, 2.05 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.25, GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def checklist_table() -> Table:
    rows = [["✓", "Section", "Part", "Material", "Qty", "Cut"]]
    items = [
        ("Skids", "Left/right skids", "4x6 PT", "2", "120\""),
        ("Base", "Long side rails", "2x6 PT", "2", "120\""),
        ("Base", "Front/rear rails", "2x6 PT", "2", "117\""),
        ("Base", "Cross ties", "2x6 PT", "3", "117\""),
        ("Posts", "Front lower-run", "4x4 PT", "3", "48\""),
        ("Posts", "Coop-front high", "4x4 PT", "3", "96\""),
        ("Posts", "Rear/low", "4x4 PT", "3", "88\""),
        ("Lower run", "Side rails", "2x4", "8", "field"),
        ("Lower run", "Door stiles", "2x4", "2", "42\""),
        ("Lower run", "Door rails", "2x4", "2", "30\""),
        ("Lower run", "Diagonal braces", "2x4", "8", "field"),
        ("Coop floor", "Front/rear rims", "2x6", "2", "120\""),
        ("Coop floor", "Joists", "2x6", "9", "45\""),
        ("Coop floor", "Floor ply main", "3/4\"", "1", "48x96\""),
        ("Coop floor", "Floor ply filler", "3/4\"", "1", "48x24\""),
        ("Coop walls", "Front plates", "2x4", "2", "120\""),
        ("Coop walls", "Front studs", "2x4", "7", "45\""),
        ("Coop walls", "Rear plates", "2x4", "2", "120\""),
        ("Coop walls", "Rear studs", "2x4", "7", "37\""),
        ("Roof", "Rafters", "2x4", "7", "60\""),
        ("Roof", "Purlins", "1x4/2x4", "4", "132\""),
        ("Roof", "Roof panels", "Corrugated", "4", "72\""),
        ("Doors", "Pop door", "1/2\" ply", "1", "12x14\""),
        ("Ramp", "Ramp deck", "1/2\" ply", "1", "14x60\""),
        ("Nest", "Nest dividers", "1/2\" ply", "3", "field"),
        ("Roosts", "Roost bars", "2x3/2x4", "2", "60–72\""),
    ]
    for sec, part, mat, qty, cut in items:
        rows.append(["☐", sec, part, mat, qty, cut])
    t = Table(rows, colWidths=[0.4 * inch, 1.0 * inch, 1.8 * inch, 1.0 * inch,
                               0.55 * inch, 1.0 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("TEXTCOLOR", (0, 0), (-1, 0), CREAM),
        ("FONTNAME", (0, 0), (-1, 0), "PF-SansBold"),
        ("FONTNAME", (0, 1), (-1, -1), "PF-Sans"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, -1), 11),
        ("FONTSIZE", (0, 1), (0, -1), 18),  # checkbox
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.4, GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


# 2026 US national-average pricing baseline. Used for the printable estimator.
COST_ITEMS = [
    ("4x6 PT skids, 10 ft", 2, 38.00),
    ("2x6 PT lumber, 10 ft", 9, 14.50),
    ("4x4 PT posts, 8 ft", 9, 16.00),
    ("2x4 exterior/treated, 8 ft", 36, 6.50),
    ("1x4 purlins, 12 ft", 4, 9.00),
    ("3/4\" exterior plywood, 4x8", 2, 72.00),
    ("1/2\" plywood or T1-11, 4x8", 5, 55.00),
    ("1/2\" 19-ga galvanized hardware cloth, 48\" x 100 ft roll", 1, 220.00),
    ("Corrugated roof panels, 36x72\"", 4, 32.00),
    ("20\" pneumatic wheels, 600 lb+", 2, 45.00),
    ("3/4\" axle + hubs / spindles set", 1, 65.00),
    ("Tow tongue + ring + safety chain set", 1, 55.00),
    ("3\" exterior structural screws (box)", 2, 18.00),
    ("1-5/8\" exterior screws (box)", 1, 12.00),
    ("1-1/4\" lath screws + fender washers", 1, 22.00),
    ("Galv bolts/washers/locknuts assortment", 1, 30.00),
    ("Heavy strap hinges", 10, 6.50),
    ("Predator-resistant latches", 9, 8.00),
    ("Nest box materials, roost bars, feeders", 1, 80.00),
    ("Exterior paint/stain + caulk + drip edge", 1, 90.00),
]


def cost_table() -> Table:
    rows = [["Item", "Qty", "Unit", "Line Total"]]
    grand = 0.0
    for name, qty, unit in COST_ITEMS:
        line = qty * unit
        grand += line
        rows.append([name, str(qty), f"${unit:,.2f}", f"${line:,.2f}"])
    rows.append(["", "", "Subtotal", f"${grand:,.2f}"])
    rows.append(["", "", "+10% waste/contingency", f"${grand * 0.10:,.2f}"])
    rows.append(["", "", "Estimated total", f"${grand * 1.10:,.2f}"])
    t = Table(rows, colWidths=[3.8 * inch, 0.55 * inch, 1.2 * inch, 1.2 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("TEXTCOLOR", (0, 0), (-1, 0), CREAM),
        ("FONTNAME", (0, 0), (-1, 0), "PF-SansBold"),
        ("FONTNAME", (0, 1), (-1, -4), "PF-Sans"),
        ("FONTNAME", (0, -3), (-1, -1), "PF-SansBold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -4), [colors.white, CREAM]),
        ("BACKGROUND", (0, -3), (-1, -3), TAN),
        ("BACKGROUND", (0, -2), (-1, -2), TAN),
        ("BACKGROUND", (0, -1), (-1, -1), GREEN),
        ("TEXTCOLOR", (0, -1), (-1, -1), CREAM),
        ("GRID", (0, 0), (-1, -1), 0.3, GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def layer_calendar_table() -> Table:
    cell = ParagraphStyle("lc", fontName="PF-Sans", fontSize=9, leading=12, textColor=CHAR)
    cellb = ParagraphStyle("lcb", fontName="PF-SansBold", fontSize=9, leading=12, textColor=GREEN)
    head = ParagraphStyle("lch", fontName="PF-SansBold", fontSize=9.5, leading=12, textColor=CREAM)
    def P(text, style=cell):
        return Paragraph(text.replace("\"", "&quot;"), style)
    raw = [
        ["Month", "Forage / Pasture", "Flock / Coop tasks"],
        ["Jan", "Dormant; rotate every 3–5 days to prevent mud", "Top up bedding, monitor frostbite, watch for pests"],
        ["Feb", "Dormant; manage mud and runoff", "Inspect hardware cloth and apron after thaws"],
        ["Mar", "First green flush; shorten rotation to 2–3 days", "Egg production rises; refresh nests, deep clean"],
        ["Apr", "Lush growth; move daily on tender pasture", "Chick brooder season; quarantine new birds"],
        ["May", "Peak growth; rotate ahead of grass going to seed", "Watch for broody hens; collect eggs twice daily"],
        ["Jun", "Heat stress risk; rotate into shade strips", "Add ventilation; frozen water bottles in nests"],
        ["Jul", "Hottest month; longer pasture rest", "Heat management; coop interior <90°F"],
        ["Aug", "Watch for forage burnout; rest paddocks", "Mid-summer mite/lice check"],
        ["Sep", "Second growth flush; resume aggressive rotation", "Molt begins; bump protein to 18–20%"],
        ["Oct", "Slowing growth; lengthen rotation", "Finish molt support; secure roof fasteners pre-storm"],
        ["Nov", "Stockpile pasture; final long graze", "Winter prep: ventilation, roost height, draft check"],
        ["Dec", "Dormant; sacrificial paddock if needed", "Light schedule decision (artificial vs natural)"],
    ]
    rows = [[P(c, head) for c in raw[0]]]
    for r in raw[1:]:
        rows.append([P(r[0], cellb), P(r[1]), P(r[2])])
    t = Table(rows, colWidths=[0.7 * inch, 2.9 * inch, 3.4 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.3, GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def broiler_schedule_table() -> Table:
    cell = ParagraphStyle("bc", fontName="PF-Sans", fontSize=8.5, leading=11, textColor=CHAR)
    cellb = ParagraphStyle("bcb", fontName="PF-SansBold", fontSize=8.5, leading=11, textColor=GREEN)
    head = ParagraphStyle("bch", fontName="PF-SansBold", fontSize=9, leading=11, textColor=CREAM)
    def P(text, style=cell):
        return Paragraph(text.replace("\"", "&quot;"), style)
    raw = [
        ["Wk", "Stage", "Feed", "Water", "Bedding / Move", "Watch for"],
        ["1", "Brooder (indoor)", "Starter 22–24%", "Quart waterer × 2", "Pine shavings; spot clean daily", "Pasty butt, chilling"],
        ["2", "Brooder", "Starter 22–24%", "1 gal waterer", "Refresh shavings; expand pen", "Coccidiosis signs"],
        ["3", "Brooder → Grower", "Transition to 20%", "1–2 gal", "Begin daylight outings if mild", "Pile-ups, drafts"],
        ["4", "Move to coop run", "Grower 20%", "5 gal in run", "Move coop every 1–2 days", "Leg/joint issues"],
        ["5", "On pasture full-time", "Grower 20%", "5 gal + drinker line", "Daily moves; fresh forage strip", "Heat stress, predators"],
        ["6", "On pasture", "Grower 19%", "Two 5 gal drinkers", "Daily moves", "Leg weakness, panting"],
        ["7", "Finisher", "Finisher 18%", "Two 5 gal drinkers", "Daily moves; rest paddock behind", "Fly load, water cleanliness"],
        ["8", "Pre-processing", "Off-feed 12 hr before", "Water until pickup", "Final move; quiet day prior", "Fasting compliance"],
    ]
    rows = [[P(c, head) for c in raw[0]]]
    for r in raw[1:]:
        rows.append([P(r[0], cellb)] + [P(c) for c in r[1:]])
    t = Table(rows, colWidths=[0.38 * inch, 1.25 * inch, 1.0 * inch, 0.95 * inch, 1.55 * inch, 1.87 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.3, GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def ensure_qr() -> Path:
    import qrcode
    qr_path = OUT_DIR / "_companion_app_qr.png"
    if not qr_path.exists():
        qr = qrcode.QRCode(border=2, box_size=12)
        qr.add_data(APP_URL)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#1F3B24", back_color="#F7F3E8")
        img.save(qr_path)
    return qr_path


# --- v1.2.0 additions -------------------------------------------------------

def economics_layer_table() -> Table:
    rows = [
        ["Layer flock economics (10 hens, year 1)", "Low", "Avg", "High"],
        ["Eggs/hen/year", "180", "240", "280"],
        ["Total eggs/year", "1,800", "2,400", "2,800"],
        ["Total dozens/year", "150", "200", "233"],
        ["Feed cost/dozen", "$2.40", "$1.80", "$1.30"],
        ["Bedding + misc/dozen", "$0.40", "$0.30", "$0.20"],
        ["Cost per dozen (op only)", "$2.80", "$2.10", "$1.50"],
        ["Local retail value/dozen (pasture-raised)", "$5.00", "$7.00", "$9.00"],
        ["Gross margin/dozen", "$2.20", "$4.90", "$7.50"],
        ["Annual gross margin (op only)", "$330", "$980", "$1,747"],
    ]
    t = Table(rows, colWidths=[3.4 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("TEXTCOLOR", (0, 0), (-1, 0), CREAM),
        ("FONTNAME", (0, 0), (-1, 0), "PF-SansBold"),
        ("FONTNAME", (0, 1), (0, -1), "PF-SansBold"),
        ("FONTNAME", (1, 1), (-1, -1), "PF-Sans"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.3, GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def economics_broiler_table() -> Table:
    rows = [
        ["Broiler economics (40-bird batch, 8 weeks)", "Low", "Avg", "High"],
        ["Chick cost/bird", "$1.80", "$2.50", "$3.50"],
        ["Feed/bird (8 wk)", "$8.00", "$11.00", "$14.00"],
        ["Bedding + misc/bird", "$1.00", "$1.50", "$2.00"],
        ["Processing/bird (DIY → custom)", "$0.50", "$4.00", "$6.50"],
        ["Total cost/bird", "$11.30", "$19.00", "$26.00"],
        ["Dressed weight (lb)", "4.5", "5.5", "6.5"],
        ["Cost/lb dressed", "$2.51", "$3.45", "$4.00"],
        ["Local retail/lb (pasture-raised)", "$5.00", "$7.00", "$9.00"],
        ["Gross margin/bird (if sold)", "$11.20", "$19.50", "$32.50"],
        ["Batch gross margin (40 birds)", "$448", "$780", "$1,300"],
    ]
    t = Table(rows, colWidths=[3.4 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("TEXTCOLOR", (0, 0), (-1, 0), CREAM),
        ("FONTNAME", (0, 0), (-1, 0), "PF-SansBold"),
        ("FONTNAME", (0, 1), (0, -1), "PF-SansBold"),
        ("FONTNAME", (1, 1), (-1, -1), "PF-Sans"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.3, GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def sourcing_table() -> Table:
    cell = ParagraphStyle("sc", fontName="PF-Sans", fontSize=8.5, leading=11, textColor=CHAR)
    cellb = ParagraphStyle("scb", fontName="PF-SansBold", fontSize=8.5, leading=11, textColor=GREEN)
    head = ParagraphStyle("sch", fontName="PF-SansBold", fontSize=9, leading=11, textColor=CREAM)
    def P(text, style=cell):
        return Paragraph(text.replace("\"", "&quot;"), style)
    raw = [
        ["Material", "Home Depot search", "Lowes search", "Tractor Supply"],
        ["4x6 PT skids, 10 ft", "4 in. x 6 in. x 10 ft #2 ground contact", "Severe Weather 4x6x10 PT", "—"],
        ["2x6 PT, 10 ft", "2 in. x 6 in. x 10 ft #2 ground contact", "Severe Weather 2x6x10 PT", "—"],
        ["4x4 PT post, 8 ft", "4 in. x 4 in. x 8 ft #2 ground contact", "Severe Weather 4x4x8 PT", "—"],
        ["2x4, 8 ft", "2 in. x 4 in. x 8 ft prime SPF", "Top Choice 2x4x8 SPF", "—"],
        ["3/4\" exterior plywood", "23/32 in. x 4x8 sanded pine plywood", "Plytanium 23/32 4x8", "—"],
        ["1/2\" T1-11 siding", "T1-11 plywood siding 4x8", "Smartside or T1-11 4x8", "—"],
        ["1/2\" HW cloth (48\"×100')", "Origin Point 1/2\" hardware cloth 48x100", "Garden Zone 1/2\" 48x100", "1/2\" galv hardware cloth 48x100"],
        ["Corrugated roof panels", "Onduline / SunTuf 36 in. polycarbonate", "Suntuf or Tuftex 36\" panel", "Galv corrugated 36\" panel"],
        ["20\" pneumatic wheels (600 lb)", "MaxPower 20 in. tire and wheel", "Kenda 20 in. tire and wheel", "Carlisle/Kenda 20\" pneumatic"],
        ["3/4\" axle rod / hub set", "Reese Tow Power 3/4 in. axle", "Reliable axle / spindle set", "Trailer axle 3/4\" hub kit"],
        ["Tow tongue + ring + chain", "Reese coupler + safety chain", "Curt coupler + safety chain", "Trailer tongue + 2-in coupler"],
        ["3\" exterior structural screws", "GRK or SPAX 3\" structural", "Power Pro 3\" structural", "—"],
        ["1-1/4\" lath screws + washers", "Pan-head lath screws #8 1-1/4\"", "Hillman lath screw + washer", "—"],
        ["Heavy strap hinges", "Everbilt 6 in. heavy strap hinge", "Stanley 6 in. heavy strap", "—"],
        ["Predator-resistant latches", "Everbilt spring-loaded gate latch", "Stanley two-step latch", "—"],
    ]
    rows = [[P(c, head) for c in raw[0]]]
    for r in raw[1:]:
        rows.append([P(r[0], cellb), P(r[1]), P(r[2]), P(r[3])])
    t = Table(rows, colWidths=[1.45 * inch, 2.05 * inch, 1.75 * inch, 1.65 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.25, GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def predator_threat_table() -> Table:
    cell = ParagraphStyle("pc", fontName="PF-Sans", fontSize=9, leading=12, textColor=CHAR)
    cellb = ParagraphStyle("pcb", fontName="PF-SansBold", fontSize=9, leading=12, textColor=GREEN)
    head = ParagraphStyle("pch", fontName="PF-SansBold", fontSize=9.5, leading=12, textColor=CREAM)
    def P(text, style=cell):
        return Paragraph(text.replace("\"", "&quot;"), style)
    raw = [
        ["Predator", "Threat profile", "Hardening upgrade beyond plans"],
        ["Raccoon", "Climbs, opens latches, reaches through 1\" wire",
         "1/2\" 19-ga hardware cloth + two-step / locking carabiner on every door"],
        ["Coyote / fox / dog", "Digs at perimeter, tests weak corners",
         "12–24\" hardware-cloth apron flat-staked outward; reinforce corner posts"],
        ["Weasel / mink", "Slips through openings ≥1\"; kills entire flocks",
         "1/2\" wire only; backed by tight gasket strip at door bottoms"],
        ["Hawk / owl", "Aerial; lifts birds out of the run during day/dusk",
         "Solid-top elevated coop already covers run; add shade-cloth top to lower run"],
        ["Snake", "Eats eggs and chicks through any gap > 1/4\"",
         "1/4\" hardware cloth around nest hatch perimeter for egg-thief seasons"],
        ["Rats / mice", "Steal feed, attract larger predators, spread disease",
         "Treadle feeders; concrete pavers under feed station; weekly perimeter scan"],
        ["Bear (where present)", "Will tear corners apart for feed and birds",
         "Solar electric fence perimeter is the only proven deterrent"],
    ]
    rows = [[P(c, head) for c in raw[0]]]
    for r in raw[1:]:
        rows.append([P(r[0], cellb), P(r[1]), P(r[2])])
    t = Table(rows, colWidths=[1.2 * inch, 2.5 * inch, 3.3 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.3, GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def winter_zone_table() -> Table:
    cell = ParagraphStyle("wc", fontName="PF-Sans", fontSize=9, leading=12, textColor=CHAR)
    cellb = ParagraphStyle("wcb", fontName="PF-SansBold", fontSize=9, leading=12, textColor=GREEN)
    head = ParagraphStyle("wch", fontName="PF-SansBold", fontSize=9.5, leading=12, textColor=CREAM)
    def P(text, style=cell):
        return Paragraph(text.replace("\"", "&quot;"), style)
    raw = [
        ["Climate zone", "Typical lows", "Coop adjustments"],
        ["Mild (Zone 8–10)", ">25°F",
         "<b>Insulation:</b> none required.<br/>"
         "<b>Water:</b> standard waterer.<br/>"
         "<b>Bedding:</b> 1\" pine shavings.<br/>"
         "<b>Moves:</b> daily or every 2 days."],
        ["Cool (Zone 6–7)", "10–25°F",
         "<b>Insulation:</b> reflective bubble in roof; foam-tape door seals.<br/>"
         "<b>Water:</b> heated waterer (125W) on thermostat.<br/>"
         "<b>Bedding:</b> 2–3\" deep-litter pine.<br/>"
         "<b>Moves:</b> every 2–4 days; sacrificial paddock if mud."],
        ["Cold (Zone 4–5)", "-10–10°F",
         "<b>Insulation:</b> 1\" foam panels in walls + draft baffles.<br/>"
         "<b>Water:</b> heated 250W on thermostat; insulated lines.<br/>"
         "<b>Bedding:</b> 4\" deep-litter, refresh weekly.<br/>"
         "<b>Moves:</b> park on south-facing pad; minimal moves Dec–Feb."],
        ["Severe (Zone 3 / 2)", "< -10°F",
         "<b>Insulation:</b> 1.5–2\" foam + radiant panel; vapor-control gap.<br/>"
         "<b>Water:</b> heated waterer + heated dog-bowl backup.<br/>"
         "<b>Bedding:</b> 6\" deep-litter + composting heat.<br/>"
         "<b>Moves:</b> park sacrificial; move only on thaw days."],
    ]
    rows = [[P(c, head) for c in raw[0]]]
    for r in raw[1:]:
        rows.append([P(r[0], cellb), P(r[1]), P(r[2])])
    t = Table(rows, colWidths=[1.35 * inch, 0.95 * inch, 4.7 * inch], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CREAM]),
        ("GRID", (0, 0), (-1, -1), 0.3, GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def signature_block() -> Table:
    rows = [
        ["Builder name (printed)", ""],
        ["Build address / parcel", ""],
        ["Build start date", ""],
        ["Build completion date", ""],
        ["Signature", ""],
        ["Date signed", ""],
    ]
    t = Table(rows, colWidths=[2.1 * inch, 4.9 * inch])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "PF-SansBold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TEXTCOLOR", (0, 0), (0, -1), GREEN),
        ("LINEBELOW", (1, 0), (1, -1), 0.6, CHAR),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))
    return t


# Build steps with subtitle + bullet sub-text. Each maps to a readable step card.
STEP_DEFS = [
    ("01", "Build the Base (10' x 10')",
     "Set the skids and perimeter — every measurement downstream depends on this.",
     "step_01_build_the_base_10_x_10.png", [
        "Lay two 4x6 PT skids parallel at 10 ft, beveled at the tow end.",
        "Cap with 2x6 PT perimeter (120\" sides, 117\" front/rear).",
        "Add three 2x6 cross ties near 48\", 72\", and 96\" from the front.",
        "Verify diagonals match within 1/4\" before going vertical.",
    ]),
    ("02", "Add Posts and Frame",
     "Nine 4x4 PT posts give the mobile coop its real backbone.",
     "step_02_add_posts_frame.png", [
        "Set three 48\" front posts, three 96\" coop-front posts, three 88\" rear posts (9 total).",
        "Tie post tops with 2x4 rails along the run sides.",
        "Add 2x4 diagonal braces at sides, rear, and coop-support line so the frame can't rack.",
    ]),
    ("03", "Build the Upper Coop Floor",
     "A solid 4x10 deck over the rear of the run becomes the elevated coop house.",
     "step_03_build_the_upper_coop_floor.png", [
        "Frame a 48\" x 120\" rim from 2x6 with 2x6 joists at ~16\" O.C.",
        "Land the floor frame on the coop-front and rear post tops over the rear 48\" of the run.",
        "Deck with 3/4\" exterior plywood (48x96\" main + 48x24\" filler). Seal edges.",
    ]),
    ("04", "Frame the Coop Walls",
     "Sloped front-to-rear walls give you the roof fall and ventilation in one move.",
     "step_04_frame_the_coop_walls.png", [
        "Front (high) wall: 2x4 plates 120\" with seven 45\" studs.",
        "Rear (low) wall: 2x4 plates 120\" with seven 37\" studs.",
        "End walls: field-cut sloped 2x4 framing from 48\" to 40\".",
        "Rough-in pop door, nest-box hatch, and rear cleanout doors.",
    ]),
    ("05", "Add Roof Framing",
     "Rafters and purlins — the structural skeleton of the corrugated roof.",
     "step_05_add_roof_to_coop.png", [
        "Cut seven 2x4 rafters at 60\" running front-to-back with overhang.",
        "Fasten through wall plates with structural screws.",
        "Add four 1x4 or 2x4 purlins at 132\" side-to-side.",
    ]),
    ("06", "Sheath the Coop",
     "Walls and roof get their first weather-tight skin.",
     "step_06_sheath_the_coop.png", [
        "Sheath walls with 1/2\" exterior plywood or T1-11; seal all cut edges.",
        "Install corrugated roof panels (~36x72\"); overlap per manufacturer.",
        "Use roofing screws with washers; add drip edge.",
    ]),
    ("07", "Install Doors and Windows",
     "Cleanout access, pop door, and ventilation — all predator-rated.",
     "step_07_install_doors_windows.png", [
        "Two large rear cleanout doors (~54x34\") for full coop access.",
        "Pop door 12x14\" with predator-resistant two-step latch.",
        "Vent and window openings backed with 1/2\" 19-ga hardware cloth.",
    ]),
    ("08", "Enclose the Run",
     "Hardware cloth — the only barrier between your flock and a determined raccoon.",
     "step_08_enclose_the_run.png", [
        "Wrap the lower run with 1/2\" 19-ga galvanized hardware cloth, 48\" wide.",
        "Fasten with lath screws + fender washers (or batten strips) every 6–8\".",
        "Optional 12–24\" fold-out apron where predators dig.",
    ]),
    ("09", "Add Wheels and Tow System",
     "Pneumatic wheels and a tow tongue turn this from a coop into a pasture rig.",
     "step_09_add_wheels.png", [
        "Mount 20\" pneumatic wheels (600 lb+ each) on 3/4\" axle or hub/spindle.",
        "Through-bolt brackets to skids; retain with washers, collars, cotter pins.",
        "Attach 4x4 (or steel) tow tongue with tow ring and safety chain at the front.",
        "Test-roll empty before adding birds.",
    ]),
    ("10", "Finish Details",
     "Paint, nests, roosts, and ramp — the buyer-ready polish pass.",
     "step_10_finish_touches.png", [
        "Paint or stain all exterior surfaces; reseal plywood cut edges.",
        "Install three nest boxes (12W x 12H x 14D) with rear access hatch.",
        "Hang 10–12 lf of removable roost bars (2x3 or 2x4).",
        "Hinge ramp deck (14x60\" with cleats every 6\") to the pop door.",
    ]),
    ("11", "Move and Rotate",
     "How to actually tow the rig without flipping it on your first cross-slope.",
     "step_11_move_rotate.png", [
        "Tow with an ATV, UTV, garden tractor, or compact tractor.",
        "Move on dry, level-ish ground; avoid steep cross-slopes.",
        "Rotate paddocks before forage is over-pecked or bedding fouls.",
    ]),
    ("12", "Broiler Setup",
     "Convert the run into a 30–45 bird grow-out tractor in under an hour.",
     "step_12_broiler_setup.png", [
        "Use the open lower run as primary space; remove or skip roosts.",
        "Provide enough feeders and waterers for the bird count.",
        "Plan shade and heat management; move the coop frequently.",
        "30–45 broilers recommended; up to ~50 only with strict management.",
    ]),
    ("13", "Layer Setup",
     "Three nests, low roosts, and a clean rear hatch — built for daily egg pulls.",
     "step_13_layer_setup.png", [
        "Three nest boxes for 10–12 hens; rear hatch for collection.",
        "Roost bars set lower than nest boxes to discourage roosting in nests.",
        "Pop door + ramp to lower run; cleanout doors for weekly bedding service.",
    ]),
    ("14", "Daily Checks",
     "The five-minute walkthrough that prevents the next predator loss.",
     "step_14_daily_checks.png", [
        "Food, water, doors, latches, and obvious predator signs every day.",
        "Spot-check hardware cloth seams and apron after storms or moves.",
        "Re-tighten wheel hardware and tongue bolts after the first week.",
    ]),
    ("15", "Maintenance and Move Schedule",
     "Weekly, monthly, seasonal — the cadence that keeps a mobile coop alive for a decade.",
     "step_15_enjoy_your_flock.png", [
        "Weekly: clean coop floor, refresh bedding, inspect roost bars and hinges.",
        "Monthly: re-seal exposed plywood edges, check roof fasteners.",
        "Seasonal: re-paint as needed, inspect skids and tongue welds/joints.",
    ]),
]


# Bullet body with a RUST accent bullet for non-step lists.
def bullet(text: str) -> Paragraph:
    return Paragraph(
        f'<font color="#8A4B2F" size="13">&#9679;</font> &nbsp;{text}',
        LIST_BODY,
    )


def build_story():
    s = []

    # Cover ----------------------------------------------------------------
    s.append(Spacer(1, 1.4 * inch))
    s.append(Paragraph("PASTUREFRAME PLANS", COVER_SUB))
    s.append(Spacer(1, 0.3 * inch))
    s.append(Paragraph("10' x 10'", COVER_TITLE))
    s.append(Paragraph("MOBILE CHICKEN COOP", COVER_TITLE))
    s.append(Spacer(1, 0.15 * inch))
    s.append(Paragraph("with 4' x 10' Elevated Coop House", COVER_SUB))
    s.append(Spacer(1, 0.6 * inch))
    s.append(Paragraph("DIY Digital Build Plans · Strict v2 Specifications", COVER_LINE))
    s.append(Paragraph("10–12 Layers · 30–45 Broilers", COVER_LINE))
    s.append(Spacer(1, 1.2 * inch))
    s.append(Paragraph("Designed by Ashton Aschenbrener", COVER_LINE))
    s.append(Paragraph(f"Version {PRODUCT_VERSION} · {date.today().isoformat()}", COVER_LINE))

    s.append(NextPageTemplate("body"))
    s.append(PageBreak())

    # Disclaimer -----------------------------------------------------------
    s.extend(chapter_h1(0, "Read First — Disclaimer",
                        "Five paragraphs that protect your build, your flock, and your money.",
                        icon_name="check"))
    s.append(Paragraph(
        "This document is a <b>digital DIY plan</b>. No physical product is shipped. "
        "These plans are provided for general DIY educational use. Site conditions, "
        "climate, wind load, snow load, soil, predator pressure, terrain, towing safety, "
        "local codes, and animal-care requirements vary by location.", BODY))
    s.append(Paragraph(
        "<b>Verify all dimensions, materials, and safety requirements for your location "
        "before building.</b> The seller does not provide professional structural "
        "certification, code-approval, permitting, animal-care, or towing-safety services. "
        "These plans are not engineered, not code-approved, not field-tested, and not "
        "predator-proof. If you live in a high-wind or heavy-snow area, consult a qualified "
        "local professional before building.", BODY))
    s.append(Spacer(1, 0.1 * inch))
    s.append(callout("safety",
        "Power tools, towing, and overhead framing all carry real risk. Eye and "
        "hearing protection are not optional, and roof framing is a two-person job."))
    s.append(Paragraph("License", H2))
    s.append(Paragraph(
        "Personal use only. No resale, redistribution, sharing, uploading to plan-trading "
        "sites, or claiming as original work. © PastureFrame Plans.", BODY))

    s.append(PageBreak())

    # TOC ------------------------------------------------------------------
    s.extend(chapter_h1(0, "Contents",
                        "Twenty-five sections, seven build phases, one mobile coop.",
                        icon_name="square"))
    toc_items = [
        ("Plan & Spec",  ["1.  Confirmed Dimensions & Capacity",
                          "2.  Tools Required",
                          "3.  Materials List (Strict v2)"]),
        ("Cut & Cost",   ["4.  Material Sourcing (HD · Lowes · TSC)",
                          "5.  Cut List (Strict v2)",
                          "6.  Cut-List Jobsite Checklist",
                          "7.  Cost Estimator (US averages)",
                          "8.  Egg & Meat Economics"]),
        ("Drawings",     ["9.  Top View",
                          "10. Side Elevation",
                          "11. Exploded Frame",
                          "12. Wheel · Skid · Tow",
                          "13. Nest & Roost Layout"]),
        ("Build",        ["14. Build Sequence — 15 Steps"]),
        ("Operate",      ["15. Layer Mode Notes",
                          "16. Broiler Mode Notes",
                          "17. Layer Rotation Calendar (12-month)",
                          "18. Broiler Grow-Out Schedule",
                          "19. Move & Rotate",
                          "20. Daily Checks & Maintenance"]),
        ("Adapt",        ["21. Predator-Proofing Addendum",
                          "22. Winterization Addendum"]),
        ("Resources",    ["23. Companion App",
                          "24. Safety, License, and FAQ",
                          "25. Builder Acknowledgment & Signature"]),
    ]
    for group, items in toc_items:
        s.append(Paragraph(group.upper(), H3))
        for item in items:
            s.append(Paragraph(item, BODY))
        s.append(Spacer(1, 0.05 * inch))
    s.append(PageBreak())

    # =====================================================================
    # PART I — PLAN & SPEC
    # =====================================================================
    s.extend(divider_page("Part I", "Plan & Spec",
                          "Confirm what you're building before you cut anything.",
                          icon_name="square"))

    # 1. Dimensions --------------------------------------------------------
    s.extend(chapter_h1(1, "Confirmed Dimensions & Capacity",
                        "The locked v2 spec — 10x10 footprint, 9 posts, 1/2\" hardware cloth.",
                        icon_name="square"))
    dim_rows = [
        ["Outside footprint", "10' x 10' (120\" x 120\")"],
        ["Lower run height", "48\" (mobile)"],
        ["Elevated coop", "4' x 10' over rear 48\""],
        ["Upper wall heights", "48\" high side / 40\" low side"],
        ["Roof fall", "approx. 8\" across 48\" depth"],
        ["Mobility", "Two 4x6 PT skids + axle pneumatic wheels + tow tongue"],
        ["Posts", "Nine 4x4 PT posts (3 front, 3 coop-front, 3 rear)"],
        ["Hardware cloth", "1/2\" 19-ga galvanized"],
        ["Layer capacity", "10–12 hens (recommended)"],
        ["Broiler capacity", "30–45 birds (recommended); up to ~50 with strict management"],
    ]
    t = Table(dim_rows, colWidths=[2.0 * inch, 5.0 * inch])
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "PF-SansBold"),
        ("FONTNAME", (1, 0), (1, -1), "PF-Sans"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TEXTCOLOR", (0, 0), (0, -1), GREEN),
        ("TEXTCOLOR", (1, 0), (1, -1), CHAR),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, GRAY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    s.append(t)
    s.append(Spacer(1, 0.15 * inch))
    s.append(callout("tip",
        "Capacity depends on breed, climate, feed/water access, and your animal-care "
        "decisions. The 30–45 broiler range assumes daily moves to fresh forage."))
    s.append(PageBreak())

    # 2. Tools -------------------------------------------------------------
    s.extend(chapter_h1(2, "Tools Required",
                        "Power, layout, and safety gear — nothing exotic, all available local.",
                        icon_name="saw"))
    s.append(Paragraph("Power & Cutting", H2))
    for b in ["Circular saw or miter saw", "Cordless drill/driver + impact driver",
              "Jigsaw (door cutouts)", "Tin snips for hardware cloth and roofing"]:
        s.append(bullet(b))
    s.append(Paragraph("Layout & Fastening", H2))
    for b in ["25 ft tape measure, framing square, speed square",
              "4 ft level, chalk line, pencil/marker",
              "Staple gun (only as a backer; lath screws + washers do the real work)",
              "Ratchet/wrench set (axle and tow hardware)",
              "Sawhorses or work table"]:
        s.append(bullet(b))
    s.append(Paragraph("PPE", H2))
    s.append(bullet("Safety glasses, hearing protection, work gloves, dust mask"))
    s.append(Spacer(1, 0.15 * inch))
    s.append(callout("mistake",
        "Trying to enclose the run with chicken wire instead of 1/2\" 19-ga hardware "
        "cloth is the #1 reason backyard flocks get raccooned. Wire choice is not a "
        "place to save money."))
    s.append(PageBreak())

    # 3. Materials ---------------------------------------------------------
    s.extend(chapter_h1(3, "Materials List (Strict v2)",
                        "The full bill of materials — buy 10% extra and don't substitute the wire.",
                        icon_name="hammer"))
    s.append(Paragraph(
        "Strict v2 supersedes earlier 6-post / 4x4-skid / caster-wheel drafts. Buy "
        "extra dimensional lumber for field-fit and mistakes.", BODY))
    s.append(Spacer(1, 0.1 * inch))
    s.append(materials_table())
    s.append(PageBreak())

    # =====================================================================
    # PART II — CUT & COST
    # =====================================================================
    s.extend(divider_page("Part II", "Cut & Cost",
                          "Source it, cut it, price it — turn the spec into a budget.",
                          icon_name="dollar"))

    # 4. Material sourcing -------------------------------------------------
    s.extend(chapter_h1(4, "Material Sourcing",
                        "Search strings for Home Depot, Lowes, and Tractor Supply.",
                        icon_name="dollar"))
    s.append(Paragraph(
        "Use these search strings at Home Depot, Lowes, and Tractor Supply to land "
        "on the right SKU fast. Brands and stocking vary by store; substitute equal "
        "or better grade. Pressure-treated lumber must be rated for ground contact "
        "anywhere it touches soil.", BODY))
    s.append(Spacer(1, 0.1 * inch))
    s.append(sourcing_table())
    s.append(Spacer(1, 0.15 * inch))
    s.append(callout("money",
        "Ask the contractor desk to bundle a 'mobile coop kit' quote. Most yards "
        "will sharpen pencils on full unit pricing for 2x4s, plywood, and hardware "
        "cloth — easy 5–10% savings."))
    s.append(PageBreak())

    # 5. Cut list ----------------------------------------------------------
    s.extend(chapter_h1(5, "Cut List (Strict v2)",
                        "Every dimension, every part — the master saw-station reference.",
                        icon_name="saw"))
    s.append(Paragraph(
        "Confirm field-fit cuts against the drawings before cutting expensive "
        "stock. Cut acceptance: diagonals match within 1/4\" before adding sheathing.",
        BODY))
    s.append(Spacer(1, 0.1 * inch))
    s.append(cut_table())
    s.append(PageBreak())

    # 6. Jobsite checklist -------------------------------------------------
    s.extend(chapter_h1(6, "Cut-List Jobsite Checklist",
                        "Print, tape to the saw station, tick as you go.",
                        icon_name="check"))
    s.append(Paragraph(
        "Print this page and tape it to the saw station. Tick each part as it's cut "
        "to the listed length. Field-fit rows leave the cut blank until the frame is up.",
        BODY))
    s.append(Spacer(1, 0.1 * inch))
    s.append(checklist_table())
    s.append(PageBreak())

    # 7. Cost estimator ----------------------------------------------------
    s.extend(chapter_h1(7, "Cost Estimator",
                        "2026 US averages — single-build quantities with a 10% contingency.",
                        icon_name="dollar"))
    s.append(Paragraph(
        "Hardcoded 2026 US national averages. Prices vary widely by region and supplier; "
        "verify locally before ordering. Total reflects single-build quantities.", BODY))
    s.append(Spacer(1, 0.1 * inch))
    s.append(cost_table())
    s.append(Spacer(1, 0.15 * inch))
    s.append(callout("money",
        "Ask the lumber yard for cull-pile 2x4s and bundle pricing on 4x4s. Hardware "
        "cloth and roofing pricing fluctuate the most — call two suppliers before ordering."))
    s.append(PageBreak())

    # 8. Economics ---------------------------------------------------------
    s.extend(chapter_h1(8, "Egg & Meat Economics",
                        "Operating margins for layers and broilers — pay back the build, then some.",
                        icon_name="dollar"))
    s.append(Paragraph(
        "Real-world ranges so you can size the operation against your goal: feed your "
        "family, sell at the gate, or run a small market flock. Numbers are operating "
        "costs only — they don't amortize the build cost from Section 7.", BODY))
    s.append(Paragraph("Layer flock", H2))
    s.append(economics_layer_table())
    s.append(Spacer(1, 0.15 * inch))
    s.append(Paragraph("Broiler batch", H2))
    s.append(economics_broiler_table())
    s.append(Spacer(1, 0.15 * inch))
    s.append(callout("money",
        "Payback math: at the avg case, layer net margin pays back the avg build "
        "cost (~$1,800 from Section 7) in roughly 2 years. A single broiler batch "
        "($780 avg margin) covers ~43% of the build in 8 weeks."))
    s.append(PageBreak())

    # =====================================================================
    # PART III — DRAWINGS
    # =====================================================================
    s.extend(divider_page("Part III", "Drawings",
                          "Five views — top, side, exploded, wheel detail, nests.",
                          icon_name="square"))

    drawings = [
        (9,  "Top-Down Plan View",       "Run + elevated coop layout, nest/roost zone, access points.",
             "dimensioned_top_view.png"),
        (10, "Side Elevation (48\" Run)", "Sloped roof, pop door, ramp, skids, and tow tongue.",
             "side_elevation_48in_run.png"),
        (11, "Exploded Frame Schematic", "Skids · base frame · 9 posts · upper coop · roof framing.",
             "exploded_frame_schematic.png"),
        (12, "Wheel · Skid · Tow Detail", "20\" pneumatic wheels on 3/4\" axle; 4x6 skids; 4x4 tow tongue with safety chain.",
             "wheel_skid_tow_tongue_detail.png"),
        (13, "Nest & Roost Layout",      "Three 12W x 12H x 14D nest boxes with rear hatch; removable roosts below nest height.",
             "nest_roost_layout.png"),
    ]
    for num, title, subtitle, fname in drawings:
        s.extend(chapter_h1(num, title, subtitle, icon_name="square"))
        img = fitted_image(DRAW / fname, 7.0 * inch, 7.2 * inch)
        img.hAlign = "CENTER"
        frame_tbl = Table([[img]], colWidths=[None])
        frame_tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CREAM),
            ("BOX", (0, 0), (-1, -1), 1.2, RUST),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))
        s.append(frame_tbl)
        s.append(Spacer(1, 0.1 * inch))
        s.append(Paragraph(subtitle, CAPTION))
        s.append(PageBreak())

    # =====================================================================
    # PART IV — BUILD
    # =====================================================================
    s.extend(divider_page("Part IV", "Build",
                          "Fifteen steps from skids to ready-to-tow.",
                          icon_name="hammer"))

    # 14. Build sequence intro --------------------------------------------
    s.extend(chapter_h1(14, "Build Sequence — 15 Steps",
                        "Each step pairs a build card with an acceptance checklist.",
                        icon_name="hammer"))
    s.append(Paragraph(
        "Each step pairs the readable build card with a checklist tied back to the "
        "strict v2 specifications and acceptance checks. Tackle one phase per work "
        "session; don't sheath until the frame is square.", BODY))
    s.append(Spacer(1, 0.15 * inch))
    s.append(callout("tip",
        "Work in sequence. Skipping ahead to roof framing before the run is square "
        "is the fastest way to fight the build. Trust the order."))
    s.append(PageBreak())

    for num, title, subtitle, fname, bullets in STEP_DEFS:
        s.extend(step_card(num, title, subtitle, STEPS / fname, bullets))
        # contextual callouts at high-leverage steps
        if num == "01":
            s.append(Spacer(1, 0.1 * inch))
            s.append(callout("mistake",
                "If diagonals don't match within 1/4\" at the base, every wall above "
                "will fight you. Re-square before going vertical."))
        elif num == "08":
            s.append(Spacer(1, 0.1 * inch))
            s.append(callout("safety",
                "1/2\" 19-ga galvanized hardware cloth is the only acceptable wire "
                "for predator zones. Chicken wire keeps chickens in — it does not "
                "keep predators out."))
        elif num == "09":
            s.append(Spacer(1, 0.1 * inch))
            s.append(callout("safety",
                "Test-roll empty before adding birds. Re-torque axle, wheel, and "
                "tongue hardware after the first 5–10 moves."))
        s.append(PageBreak())

    # =====================================================================
    # PART V — OPERATE
    # =====================================================================
    s.extend(divider_page("Part V", "Operate",
                          "Run the rig — layers, broilers, rotation, daily care.",
                          icon_name="chicken"))

    # 15. Layer mode -------------------------------------------------------
    s.extend(chapter_h1(15, "Layer Mode Notes",
                        "10–12 hens, three nests, low roosts — the daily egg pull.",
                        icon_name="chicken"))
    for p in [
        "Recommended for 10–12 hens. Use all three nest boxes and the full roost set.",
        "Set roost bars below the nest-box opening to keep hens off the nests at night.",
        "Collect eggs through the rear nest hatch; line nests with clean shavings or pine.",
        "Verify pop door closes and locks each night. Add a manual dawn/dusk routine before any automated door is considered.",
    ]:
        s.append(Paragraph(p, BODY))
    s.append(PageBreak())

    # 16. Broiler mode -----------------------------------------------------
    s.extend(chapter_h1(16, "Broiler Mode Notes",
                        "30–45 birds, no roosts, daily moves to fresh forage.",
                        icon_name="broiler"))
    for p in [
        "Recommended for 30–45 broilers. Up to ~50 only with frequent moves, strong ventilation, sufficient feeders/waterers, shade, and heat management.",
        "Use the open lower run as the primary living space; remove or skip roost bars.",
        "Move the coop daily or every other day onto fresh forage when birds are growing.",
        "Watch for heat stress in summer: shade-cloth side, frozen water bottles, and shade-side rotation are all standard practice — verify your climate.",
    ]:
        s.append(Paragraph(p, BODY))
    s.append(Spacer(1, 0.15 * inch))
    s.append(callout("safety",
        "Broilers are heat-sensitive. Coop interior >90°F is a fatal risk by week 6. "
        "Plan shade and ventilation before chick day."))
    s.append(PageBreak())

    # 17. Layer rotation calendar -----------------------------------------
    s.extend(chapter_h1(17, "Layer Rotation Calendar",
                        "Twelve months of pasture and flock cadence.",
                        icon_name="calendar"))
    s.append(Paragraph(
        "Generic Northern-Hemisphere temperate-zone schedule. Shift +/- 1 month for "
        "your latitude. Verify locally; this is guidance, not a code.", BODY))
    s.append(Spacer(1, 0.1 * inch))
    s.append(layer_calendar_table())
    s.append(PageBreak())

    # 18. Broiler grow-out -------------------------------------------------
    s.extend(chapter_h1(18, "Broiler Grow-Out Schedule",
                        "Eight-week Cornish-cross schedule, week-by-week.",
                        icon_name="calendar"))
    s.append(Paragraph(
        "Cornish-cross style 8-week schedule. Slow-growth breeds run 10–12 weeks; "
        "extend Weeks 4–6 by one week each. Always verify with your hatchery and vet.",
        BODY))
    s.append(Spacer(1, 0.1 * inch))
    s.append(broiler_schedule_table())
    s.append(PageBreak())

    # 19. Move & rotate ----------------------------------------------------
    s.extend(chapter_h1(19, "Move & Rotate",
                        "How to tow without flipping and how to rotate without trashing pasture.",
                        icon_name="hammer"))
    for p in [
        "Tow with an ATV, UTV, garden tractor, or compact tractor. Walk the move route first.",
        "Avoid steep cross-slopes; the upper coop raises the center of gravity.",
        "Rotate paddocks before forage is over-pecked or bedding fouls. A simple field map plus a moves-per-week target prevents over-grazing one strip.",
        "After the first 5–10 moves: re-torque axle, wheel, and tow-tongue hardware.",
    ]:
        s.append(Paragraph(p, BODY))
    s.append(PageBreak())

    # 20. Daily checks -----------------------------------------------------
    s.extend(chapter_h1(20, "Daily Checks & Maintenance",
                        "Daily, weekly, seasonal — the cadence that keeps birds alive.",
                        icon_name="check"))
    s.append(Paragraph("Daily", H2))
    for b in ["Food, water, and ventilation",
              "Doors, latches, and pop door function",
              "Bird count and obvious predator signs"]:
        s.append(bullet(b))
    s.append(Paragraph("Weekly", H2))
    for b in ["Refresh bedding and clean coop floor",
              "Inspect hardware-cloth seams and door hinges",
              "Confirm wheels roll free and tongue bolts are tight"]:
        s.append(bullet(b))
    s.append(Paragraph("Seasonal", H2))
    for b in ["Re-paint or re-seal exposed plywood edges",
              "Inspect roof fasteners after any major storm",
              "Inspect skids and tongue connections for splits or rust"]:
        s.append(bullet(b))
    s.append(PageBreak())

    # =====================================================================
    # PART VI — ADAPT
    # =====================================================================
    s.extend(divider_page("Part VI", "Adapt",
                          "Predator pressure and winter — harden the build for your site.",
                          icon_name="paw"))

    # 21. Predator-proofing addendum --------------------------------------
    s.extend(chapter_h1(21, "Predator-Proofing Addendum",
                        "Threat profiles and hardening upgrades — region by region.",
                        icon_name="paw"))
    s.append(Paragraph(
        "These plans are not predator-proof. The base spec uses 1/2\" 19-ga "
        "hardware cloth, a solid elevated coop, and two-step latches — all best "
        "practice — but predator pressure varies by region, season, and night. "
        "This addendum lists upgrades you should evaluate against your local "
        "threats <i>before</i> losing birds, not after.", BODY))
    s.append(Spacer(1, 0.1 * inch))
    s.append(predator_threat_table())
    s.append(Spacer(1, 0.15 * inch))
    s.append(Paragraph("Layered defense rules of thumb", H2))
    for b in [
        "Wire mesh openings ≤ 1/2\" everywhere a small predator can press a snout.",
        "Every door takes two independent actions to open (eg. spring latch + carabiner).",
        "Apron flares 12–24\" outward at ground; staked flat; not buried.",
        "Lock-up at dusk is non-negotiable. Even 'safe' yards lose birds to dawn/dusk hawk passes.",
        "If you lose a bird, walk the entire perimeter the next morning. Predators return.",
    ]:
        s.append(bullet(b))
    s.append(PageBreak())

    # 22. Winterization addendum ------------------------------------------
    s.extend(chapter_h1(22, "Winterization Addendum",
                        "Match your build spec to the coldest week your site sees.",
                        icon_name="snowflake"))
    s.append(Paragraph(
        "Match your build spec to the coldest week your site sees, not the average. "
        "Chickens tolerate cold far better than wet drafts; the goal is dry air, "
        "liquid water, and a coop interior that stays above ~10°F at night.", BODY))
    s.append(Spacer(1, 0.1 * inch))
    s.append(winter_zone_table())
    s.append(Spacer(1, 0.15 * inch))
    s.append(callout("winter",
        "Ventilation > insulation. A sealed coop traps ammonia and moisture and "
        "frostbites combs. Keep vents high (above bird height) and small enough "
        "that snow doesn't blow in."))
    s.append(Paragraph("Universal winter rules", H2))
    for b in [
        "Open water 24/7. A frozen waterer kills production faster than the cold itself.",
        "Deep-litter the coop floor: start at 2\" and add fresh shavings weekly through winter.",
        "Comb protection: pure petroleum jelly on combs/wattles below 0°F for large-comb breeds.",
        "Power: a heated waterer + thermostatic outlet beats running a heat lamp (fire risk).",
    ]:
        s.append(bullet(b))
    s.append(PageBreak())

    # =====================================================================
    # PART VII — RESOURCES
    # =====================================================================
    s.extend(divider_page("Part VII", "Resources",
                          "Companion app, FAQ, license, and your builder signature.",
                          icon_name="app"))

    # 23. Companion app ----------------------------------------------------
    s.extend(chapter_h1(23, "Companion App",
                        "PastureFrame Coop Build Companion — free web app, works on your phone.",
                        icon_name="app"))
    s.append(Paragraph(
        "PastureFrame Coop Build Companion is a free web app that walks you through "
        "the same 15 steps with check-off tracking and quick reference to materials and "
        "cut lengths. Open it on your phone at the jobsite.", BODY))
    s.append(Spacer(1, 0.15 * inch))
    qr_path = ensure_qr()
    qr_img = RLImage(str(qr_path))
    qr_img.drawWidth = 2.5 * inch
    qr_img.drawHeight = 2.5 * inch
    qr_img.hAlign = "CENTER"
    s.append(qr_img)
    s.append(Spacer(1, 0.1 * inch))
    s.append(Paragraph(f"<para alignment='center'><b>{APP_URL}</b></para>", BODY))
    s.append(Spacer(1, 0.1 * inch))
    s.append(callout("tip",
        "If a step in the app ever disagrees with this PDF, the PDF is the source "
        "of truth. The app is provided free and as-is."))
    s.append(PageBreak())

    # 24. Safety / FAQ -----------------------------------------------------
    s.extend(chapter_h1(24, "Safety, License, and FAQ",
                        "The fine print and the questions everyone asks.",
                        icon_name="check"))
    s.append(Paragraph("Safety", H2))
    s.append(Paragraph(
        "Power tools, towing, and overhead framing all carry real risk. Work with a partner "
        "for sheet-good handling and roof framing. Do not stand under unsecured rafters. "
        "Eye and hearing protection are not optional.", BODY))
    s.append(Paragraph("Predator & weather caution", H2))
    s.append(Paragraph(
        "No coop is fully predator-proof. Use 1/2\" 19-ga hardware cloth (not chicken wire) "
        "for predator zones, two-step latches on every exterior door, and a 12–24\" "
        "hardware-cloth apron where predators dig. In high-wind or heavy-snow regions, "
        "consult a qualified local professional before building.", BODY))
    s.append(Paragraph("Frequently asked", H2))
    for q, a in [
        ("Is this a physical coop?", "No. This is a digital plans package. You receive PDF files only."),
        ("Can I use this for broilers?", "Yes. See Section 16. Broilers use the open run; remove or skip roosts."),
        ("Is it walk-in?", "No. The mobile version uses a 48\" lower run to keep the center of gravity low for towing."),
        ("How long to build?", "Most builders finish over 2–3 weekends with intermediate carpentry skills."),
        ("Refunds?", "Per Etsy policy for digital downloads, sales are generally final once files are accessed. Message first if you have a problem."),
        ("Can I share these plans?", "No. Personal use only."),
    ]:
        s.append(Paragraph(f"<b>{q}</b>", BODY))
        s.append(Paragraph(a, BODY))

    s.append(Paragraph("License", H2))
    s.append(Paragraph(
        "© PastureFrame Plans. Personal use only. No resale, redistribution, sharing, "
        "uploading to plan-trading sites, or claiming as original work.", BODY))
    s.append(PageBreak())

    # 25. Builder acknowledgment & signature ------------------------------
    s.extend(chapter_h1(25, "Builder Acknowledgment & Signature",
                        "Optional but recommended — sign it and keep it with your build records.",
                        icon_name="signature"))
    s.append(Paragraph(
        "Optional but recommended. Print this page, fill it in, and keep it with "
        "your build records. By signing below the builder acknowledges that:", BODY))
    for b in [
        "These plans are digital DIY guidance, not engineered or code-approved drawings.",
        "Verification of all dimensions, materials, and applicable local codes is the builder's responsibility.",
        "PastureFrame Plans and Ashton Aschenbrener are not liable for site conditions, towing safety, predator events, animal-care outcomes, or weather-related damage.",
        "These plans are licensed for personal use only and may not be resold or redistributed.",
    ]:
        s.append(bullet(b))
    s.append(Spacer(1, 0.25 * inch))
    s.append(signature_block())
    s.append(Spacer(1, 0.3 * inch))
    s.append(Paragraph("— End of plan —", CAPTION))

    return s


def main():
    doc = make_doc(OUT)
    doc.build(build_story())
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
