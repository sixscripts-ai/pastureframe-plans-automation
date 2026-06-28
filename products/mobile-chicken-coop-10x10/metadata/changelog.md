# Changelog — 10x10 Mobile Chicken Coop Plans

## v1.0.0 — 2026-06-26
- Initial draft package: outline, materials list, cut list, listing copy, FAQ,
  10 image concepts, PDF table of contents, and disclaimers.
- Added chicken coop step-image source assets: 15 original crops, 15 readable
  step cards, and contact sheets under `source/images`.
- Updated PDF table of contents to match the 15-card chicken coop build
  sequence.
- Applied PastureFrame Plans brand, Ashton designer credit, conservative
  10-12 layer / 30-45 broiler capacity, 48"-54" mobile lower-run height,
  skid-and-wheel mobility, and 1/2" 19-gauge main hardware-cloth spec.
- Pending: original CAD drawings (Ashton), original photographs, image
  exports, compliance review pass, listing draft creation.

## v1.0.0-strict-v2 — 2026-06-27
- Imported `pastureframe_chicken_coop_final_plan_package.zip` into
  `final_plan_package/` with all package docs, CSV checklists, drawing assets,
  current draft plan PDF, original infographic, original CSVs, and step-image ZIP.
- Replaced active `source/spreadsheets/materials.md` with strict materials list
  v2 from the imported package.
- Replaced active `source/spreadsheets/cut-list.md` with strict cut list v2 from
  the imported package.
- Locked source-of-truth decisions for automation: 48" lower run height, 4x6
  skids, axle-mounted pneumatic wheels, tow tongue, nine 4x4 posts, 1/2" 19-ga
  galvanized hardware cloth, and CAD/plans-first sales status.
- Superseded older 6-post, 4x4-skid, caster-wheel, 48"-54" lower-run, and 1/4"
  main-mesh draft specs. Agents must not use them.

## v1.1.0 — 2026-06-27
- Composed final buyer-facing PDF v1.1.0 (39 pages, ~15 MB).
- Added cut-list jobsite checklist (printable big-checkbox table).
- Added cost estimator with 2026 US national-average prices, +10% waste,
  estimated total.
- Added 12-month layer rotation calendar.
- Added 8-week broiler grow-out schedule (Cornish-cross baseline).
- Added Companion App page with QR code + URL
  (https://pastureframe-coop-build-companion.vercel.app/).
- Composed 10 Etsy listing tiles (2000x2000) at
  `deliverables/etsy_listing_images/`.
- Renumbered TOC to 20 sections; FAQ section reference updated.
- Set launch pricing ladder $29 (launch) → $39 (regular) → $49 (premium);
  updated `price` to 29 and added `pricing_ladder` block in `metadata/listing.json`.
- Pointed `files.main_pdf` to the v1.1.0 deliverable PDF.
- Rewrote `source/copy/listing.md` to advertise the new value-adds and the
  $29 launch tier; preserved compliance language (plans-only, not engineered,
  not field-tested, not predator-proof).

## v1.2.0 — 2026-06-27
- Composed final buyer-facing PDF v1.2.0 (45 pages, ~15 MB).
- Added Section 4 — Material Sourcing sheet: Home Depot · Lowes · Tractor Supply
  search strings for every key material.
- Added Section 8 — Egg & Meat Economics: layer cost-per-dozen and broiler
  cost-per-lb tables (low / avg / high) plus payback math.
- Added Section 21 — Predator-Proofing Addendum: threat-by-threat hardening
  matrix (raccoon, coyote, weasel, hawk, snake, rats, bear) + layered defense
  rules.
- Added Section 22 — Winterization Addendum: climate-zone matrix
  (Zone 8–10 → Zone 2/3) for insulation, water plan, bedding, move cadence.
- Added Section 25 — Builder Acknowledgment & Signature page (printable, with
  liability acknowledgments).
- Renumbered TOC to 25 sections; updated FAQ broiler section reference to 16.
- Pointed `files.main_pdf` to the v1.2.0 deliverable PDF; bumped
  `metadata/listing.json` `version` to 1.2.0.
- Rewrote `source/copy/listing.md` opening, page count (45), and What's Included
  bullets to advertise the five new sections; updated SEO title to feature the
  cost estimator and the predator/winter addenda.

## v2.0.0 — 2026-06-27
- Major design system upgrade: new "Modern PastureFrame" v2 design language
  applied across the manual. Composed v2.0.0 PDF (65 pages, ~15.45 MB).
- Authored reusable design skill at
  `~/.trae/skills/diy-build-manual-design/SKILL.md` so future build manuals
  inherit the same type ramp, palette, divider-page system, branded step
  cards, callouts, and icon set.
- Type ramp bumped across the board: body 12/17 floor (up from 9/12), H1 30/36,
  H2 16/22, H3 13/18, plus decorative italic chapter subtitles (RUST 14/20).
- Expanded accent palette: SUN #E8B23C, SKY #4A7A8C, CLAY #B85440, MOSS
  #6E8C58 — used for themed callouts.
- Added 7 section divider pages (Plan & Spec, Cut & Cost, Drawings, Build,
  Operate, Adapt, Resources) with full-bleed CREAM background, GREEN top bar,
  TAN bottom bar, large display numerals, and chapter icon.
- Added 5 callout types (PRO TIP, COMMON MISTAKE, SAFETY, WINTER NOTE, MONEY
  MOVE) with themed accent bars; 12 callouts placed throughout the manual.
- Branded step cards: every build step gets a one-line italic subtitle plus a
  CREAM-bg / RUST-bordered image frame and a GREEN "ACCEPTANCE CHECKLIST"
  badge bar above bullets.
- Custom 13-icon transparent PNG set at `products/_shared/icons/` (saw, hammer,
  drill, square, chicken, broiler, snowflake, paw, dollar, calendar, check,
  app, signature) generated by `scripts/compose/make_icons.py`.
- TOC regrouped under the seven part labels for visual scanning.
- Drawings now framed with the same RUST/CREAM treatment as step-card images
  for layout consistency.
- Pointed `files.main_pdf` to the v2.0.0 deliverable PDF; bumped
  `metadata/listing.json` `version` to 2.0.0.
- Updated `source/copy/listing.md` page count from 45 → 65 in opening, short
  description, attributes, and What's Included header.

## v2.0.0 (layout fix pass) — 2026-06-27
- Removed baked-in "DRAFT PLAN ASSET" / "DRAWING REQUIREMENT" overlays from
  `dimensioned_top_view.svg`, `side_elevation_48in_run.svg`, and
  `exploded_frame_schematic.svg`; re-rasterized PNGs via
  `scripts/compose/clean_drawing_svgs.py`.
- Fixed materials table wire-row overlap (wider Category/Qty columns, shortened
  HW-cloth label) and sourcing-table hardware-cloth row wrap.
- Redesigned winterization table from 6 cramped columns to a readable 3-column
  zone checklist layout.
- Regenerated v2.0.0 PDF (68 pages, ~15.52 MB). Updated listing page count.
