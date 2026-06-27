# 15 — Image Template System

See also: [templates/images/template_brief.md](../templates/images/template_brief.md).

## Pipeline
1. **Ashton** designs the original render or photographs the built unit.
2. Layered Figma file at `assets/brand/listing-image-templates.fig`
   (operator-managed) holds the 10 slot layouts.
3. Export PNGs at 2000x2000 to `products/[slug]/exports/listing-images/`.
4. Listing Agent references slot definitions to write image alt-text and
   image-brief copy.
5. Compliance Agent flags any hero export that does not include the
   "DIGITAL PLANS" overlay (operator-confirmed checkbox in `seo.json`).

## Compliance Hard Rules
- Hero MUST display "DIGITAL PLANS" prominently.
- No third-party brand logos in any slot.
- No stock photography (Etsy 2026 listing image policy).
- AI-assisted exports must carry a small "AI-assisted" mark and disclosure
  in the listing description.

## Slot Definitions
See `templates/images/template_brief.md` for the 10-slot table.
