# 05 — Etsy Store Setup Package

## Account Setup Checklist (manual, performed by Ashton)
- [ ] Create Etsy seller account using business email.
- [ ] Choose shop name: **PastureFrame Plans**.
- [ ] Set shop language: English; primary currency: USD.
- [ ] Complete payment & tax info (Etsy Payments).
- [ ] Confirm bank account.
- [ ] Confirm 2FA on the Etsy account.
- [ ] Upload shop logo (square, 500x500 minimum).
- [ ] Upload shop banner (1200x300 minimum).
- [ ] Write About section (Ashton + the homestead origin story; disclose any AI assistance per Etsy 2026 Seller Policy).
- [ ] Set Shop Policies:
  - Returns/Refunds (digital downloads — case-by-case, contact first).
  - Privacy.
  - Shop policies disclosing personal-use license.
- [ ] Create and verify the **PastureFrame Plans Automation** Etsy Developer App at https://www.etsy.com/developers/register.
  - Save keystring + shared secret in your secret manager.
  - Development redirect URI: `http://localhost:3000/api/etsy/callback`.
  - Production redirect URI: `https://pastureframeplans.com/api/etsy/callback` unless the final domain changes.
  - Minimum MVP scopes: `listings_r listings_w shops_r shops_w transactions_r`.

## About Section Draft (Ashton edits)
> I'm Ashton Aschenbrener, designer behind PastureFrame Plans. I create
> practical digital plans for mobile coops and homestead structures: clear
> dimensions, build steps, material lists, and pasture-ready layouts for DIY
> builders. Every plan is a digital download for personal use and should be
> verified locally before building.
>
> AI disclosure: I use AI tools to help draft listing copy and concept
> images. Plans, dimensions, and build notes are designed by Ashton
> Aschenbrener.

## Shop Policies (drafts — operator must review with attorney/CPA before publishing)
- Returns/Refunds: Per Etsy's policy on digital downloads, sales are
  generally final once files are accessed. Contact us first if there is a
  problem; we will help where we can.
- Privacy: We never share your information. Buyer identifiers we store are
  hashed.
- Shipping: All products are digital. No physical shipments.
- License: Personal use only. No resale, redistribution, or sharing.

## Initial Listing Plan (first 4 listings)
1. 10x10 Mobile Chicken Coop Plans (flagship) — $39
2. Garden Shade Roof — $19 (secondary/backlog until coop listing is ready)
3. Raised Garden Bed (simple) — $9
4. Broiler Tractor — $29

Bundle to introduce in week 3:
- "Starter Homestead Bundle" (coop + bed + shade roof) — $59
