# 02 — Compliance Research Memo

**Last reviewed:** 2026-06-26
**Sources:** Official Etsy Seller Policy (effective 2026-07-09), Prohibited
Items Policy (effective until 2026-08-11), Intellectual Property Policy,
Etsy Open API v3 documentation, Etsy Seller Handbook AI disclosure article.

> This memo is a living document. Re-check Etsy's policy pages quarterly and
> immediately before any major release. Etsy can change policies on short
> notice, and they reserve the right to remove listings or suspend shops.

## 1. What Etsy Allows for Our Business
- **Digital downloads are explicitly supported.** Etsy's Listings Tutorial
  documents `type: "download"` listings; the Fulfillment Tutorial confirms
  no shipping action is required for digital products and that buyers can
  re-download files indefinitely from purchase history.
- **Plans, designs, and templates designed by the seller are allowed.**
  Items must be "made, designed, handpicked, or sourced by a seller." Plans
  Ashton designs himself qualify under "designed."

## 2. What Etsy Requires of Us
1. **Transparent representation of how items are made and by whom.** Our
   shop About section must accurately describe Ashton and any shop members.
2. **Original photographs.** No stock photos in listing images. Limited
   exceptions exist for production-partner items; not relevant to us. Our
   listing images must be Ashton's own renders, photos, or original graphics.
3. **AI disclosure.** If generative AI is used in creating the product, we
   must disclose it in the listing. Our policy: AI may assist drafting copy
   and image concepts but Ashton designs the actual plans. We will mark
   listings as "AI-assisted" when AI is materially involved in plan content,
   per the Seller Handbook AI article.
4. **Production partner disclosure** if any external party assists in making
   plans. Currently N/A; revisit if Ashton hires designers.
5. **Accurate digital-product description.** Buyer must understand they
   receive digital files only.
6. **No dropshipping or reselling** (allowed exceptions don't apply here).
7. **No gift cards, no off-Etsy referral codes, no want-ads.**

## 3. Etsy Open API v3 — Key Constraints
- **Auth:** OAuth 2.0 Authorization Code Grant **with PKCE**. Tokens issued
  via `https://api.etsy.com/v3/public/oauth/token`. Refresh grants supported.
  We must never log access tokens.
- **API key:** Every request requires the `x-api-key` header carrying the
  app's keystring (and shared secret, colon-separated, per Etsy docs).
- **Scopes (least privilege we need):**
  `listings_r listings_w shops_r shops_w transactions_r`.
  Do not request `transactions_w` until fulfillment/write actions are truly in
  scope.
  Add `email_r` only if buyer email surfaces are needed (commercial-access only).
- **Personal Access** is sufficient (we manage one shop). Up to 5 shops allowed.
- **Dormancy:** App is banned after 6 months without a successful API call.
  Mitigation: a daily heartbeat call to `getShop`.
- **Caching policy and trademark disclosure** required for commercial-access
  apps. We are personal-access; still good practice to add an attribution
  string in any external-facing UI: *"The term 'Etsy' is a trademark of
  Etsy, Inc. This application uses the Etsy API but is not endorsed or
  certified by Etsy, Inc."*
- **No screen scraping.** All Etsy data flows through the Open API only.
- **Rate limits:** Etsy enforces per-app request budgets. Implement
  exponential backoff and respect `Retry-After`.

## 4. Listing Field Requirements (Digital Download)
Required for `createDraftListing`:
- `quantity` (use a high number like 999 for unlimited digital sales)
- `title`, `description`, `price`
- `who_made` (use `i_did` since Ashton designs the plans)
- `when_made` (use `made_to_order` for newly drafted plans)
- `taxonomy_id` (Etsy taxonomy id; for plans, use a "Patterns / How-to"
  taxonomy node — verify with `getSellerTaxonomyNodes` at runtime)
- `type` set to `download` via `updateListing` after creation
- At least one listing image
- 13 tags max (Etsy limit), each ≤ 20 characters, no special characters

## 5. Hard Compliance Rules for Our Shop
1. Every listing image **must clearly say "DIGITAL PLANS"** (especially the
   hero) so buyers cannot confuse the product with a physical structure.
2. Every listing description **must include**:
   - "This is a digital download. No physical product will be shipped."
   - "Buyer receives plan files only."
   - "Personal use only — no resale, redistribution, or sharing."
   - The standard DIY/codes/safety disclaimer.
3. **No engineering, code-approval, or stamped claims.** Our plans are not
   stamped by a licensed engineer and we will not say or imply they are.
4. **No specific load ratings (snow, wind, seismic) without verified
   engineering review.** General guidance phrased as "verify locally" only.
5. **No animal-welfare medical/veterinary claims.** Husbandry guidance is
   general DIY only.
6. **Intellectual property:** All drawings, copy, and images must be
   Ashton-original. No copying competitor descriptions or plan sets.
7. **Privacy:** Hash buyer identifiers in our DB. Never send raw PII to LLMs;
   redact via the [src/lib/redact.ts](../src/lib/redact.ts) helper.
8. **AI disclosure:** When AI materially shapes a plan or image, list the
   product as AI-assisted in the listing description.

## 6. Prohibited / Restricted Items (We Don't Sell Any of These)
Alcohol, tobacco, drugs, weapons, hate items, items glorifying violence,
nudity/sexual content, regulated medical items, animal products, hazardous
materials, currency, securities, lottery tickets. Our digital plans for
animal housing fall outside the prohibited list, but we must avoid:
- Plans for trapping or harming protected wildlife.
- Husbandry guidance crossing into veterinary medical claims.

## 7. Buyer Messaging Rules
- Etsy's Communication Standards prohibit harassment, off-platform diversion
  of transactions (without exception), spam, and sharing of private data.
- Etsy's Case System governs disputes; we should not promise outcomes
  outside that system.
- Reviews: do not solicit or incentivize reviews (no "leave a 5-star review
  for a discount").

## 8. Refunds and Cases
- For digital downloads, Etsy's general guidance is that all sales are
  final, but sellers can issue refunds at their discretion through the Etsy
  refund flow. Our policy: refund requests are HIGH-RISK and require human
  approval before any response.

## 9. Commercial vs Personal Access
We will operate under **Personal Access** (one shop, Ashton's). If we ever
build the system for other sellers, we must apply for Commercial Access and
add the trademark notice and caching policy described in Etsy's docs.

## 10. Action Items From This Memo
- [ ] Add the standard plan disclaimer to every listing template.
- [ ] Add "DIGITAL PLANS" overlay rule to every image template.
- [ ] Implement OAuth 2.0 + PKCE in [src/api/etsy/oauth.ts](../src/api/etsy/oauth.ts).
- [ ] Implement daily heartbeat job to avoid app dormancy.
- [ ] Implement `Retry-After`-aware backoff in [src/api/etsy/client.ts](../src/api/etsy/client.ts).
- [ ] Implement PII redactor in [src/lib/redact.ts](../src/lib/redact.ts).
- [ ] Add AI-assisted disclosure block to listing template.

## References
- Etsy Open API v3 Authentication: https://developer.etsy.com/documentation/essentials/authentication/
- Etsy Open API v3 Listings Tutorial: https://developer.etsy.com/documentation/tutorials/listings/
- Etsy Open API v3 Fulfillment Tutorial: https://developer.etsy.com/documentation/tutorials/fulfillment/
- Etsy Seller Policy (effective 2026-07-09): https://www.etsy.com/legal/sellers/
- Etsy Prohibited Items Policy: https://www.etsy.com/legal/prohibited/
- Etsy Intellectual Property Policy: https://www.etsy.com/legal/ip/
- Etsy Seller Handbook on AI: https://www.etsy.com/seller-handbook/article/1275449912004
