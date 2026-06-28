"""Remove draft overlay boxes from plan drawing SVGs and re-rasterize PNGs."""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRAW = ROOT / "products" / "mobile-chicken-coop-10x10" / "final_plan_package" / "drawing_assets"
SVG_DIR = DRAW / "svg"
PNG_DIR = DRAW / "png"

# Draft / proof overlays baked into source SVGs.
DRAFT_SNIPPETS = [
    # dimensioned_top_view — bottom-left callout
    r'<rect x="50" y="760" width="330" height="250" fill="#FFFFFF" stroke="#7D8178" stroke-width="2"/>'
    r'<text x="75" y="800" class="t" text-anchor="start">DRAFT PLAN ASSET</text>'
    r'<text x="75" y="840" class="small" text-anchor="start">Use as first dimensioned top-view proof\.</text>'
    r'<text x="75" y="875" class="small" text-anchor="start">Replace or polish with CAD before launch\.</text>'
    r'<text x="75" y="925" class="small" text-anchor="start">Final locked height is controlled by side view\.</text>',
    # side_elevation — upper-left callout covering roof detail
    r'<rect x="70" y="165" width="380" height="145" fill="#FFFFFF" stroke="#7D8178" stroke-width="2"/>'
    r'<text x="95" y="205" class="t" text-anchor="start">DRAFT PLAN ASSET</text>'
    r'<text x="95" y="245" class="small" text-anchor="start">Final mobile plan uses 48 in lower run\.</text>'
    r'<text x="95" y="280" class="small" text-anchor="start">54 in or 72 in variants require new cut list\.</text>',
    # exploded_frame — upper-left requirement box
    r'<rect x="70" y="160" width="390" height="190" fill="#FFFFFF" stroke="#7D8178" stroke-width="2"/>'
    r'<text x="100" y="205" class="t" text-anchor="start">DRAWING REQUIREMENT</text>'
    r'<text x="100" y="245" class="small" text-anchor="start">This schematic is a draft proof asset\.</text>'
    r'<text x="100" y="280" class="small" text-anchor="start">A final CAD exploded view should replace it\.</text>'
    r'<text x="100" y="315" class="small" text-anchor="start">Must show brace locations and lumber sizes\.</text>',
    # exploded_frame — callout boxes/lines crossing layer 2 (render as red X artifacts)
    r'<line x1="1140" y1="730" x2="1000" y2="610" stroke="#8A4B2F" stroke-width="6"/>'
    r'<text x="1120" y="640" class="small" text-anchor="start">diagonal braces shown in rust</text>'
    r'<rect x="400" y="620" width="190" height="85" fill="none" stroke="#7D8178" stroke-width="2"/>'
    r'<rect x="910" y="620" width="190" height="85" fill="none" stroke="#7D8178" stroke-width="2"/>'
    r'<text x="410" y="735" class="small" text-anchor="start">hardware cloth panels</text>',
]

# Remaining diagonal brace callout line crossing layer 2.
EXTRA_LINE_PATTERNS = [
    r'<line x1="360" y1="730" x2="500" y2="610" stroke="#8A4B2F" stroke-width="6"/>',
]


def strip_draft_markup(svg_text: str) -> str:
    out = svg_text
    for snippet in DRAFT_SNIPPETS + EXTRA_LINE_PATTERNS:
        out = re.sub(snippet, "", out)
    return out


def rasterize_svg(svg_path: Path, png_path: Path, width: int = 1600) -> None:
    out_dir = png_path.parent
    subprocess.run(
        ["qlmanage", "-t", "-s", str(width), "-o", str(out_dir), str(svg_path)],
        check=True,
        capture_output=True,
    )
    produced = out_dir / f"{svg_path.name}.png"
    if not produced.exists():
        raise FileNotFoundError(f"qlmanage did not produce {produced}")
    produced.replace(png_path)


def main() -> None:
    targets = [
        "dimensioned_top_view.svg",
        "side_elevation_48in_run.svg",
        "exploded_frame_schematic.svg",
    ]
    for name in targets:
        svg_path = SVG_DIR / name
        png_path = PNG_DIR / name.replace(".svg", ".png")
        bak = png_path.with_suffix(png_path.suffix + ".bak")
        if not bak.exists() and png_path.exists():
            shutil.copy(png_path, bak)

        original = svg_path.read_text()
        cleaned = strip_draft_markup(original)
        if cleaned == original:
            print(f"no draft markup removed: {name}")
        else:
            svg_path.write_text(cleaned)
            print(f"cleaned SVG: {name}")

        rasterize_svg(svg_path, png_path)
        print(f"rasterized: {png_path.name}")


if __name__ == "__main__":
    main()