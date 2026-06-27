# 18 — Operating Manual

## 1. Add a New Product Idea
1. Add a row to `products` with `status='idea'` and a slug.
2. Optional: run `npm run agent:product` to draft a starter package.
3. Move to `status='draft'` once you have specifications locked.

## 2. Approve a Product
1. Review the draft in `/products/[slug]/source/`.
2. Confirm CAD drawings and original photographs are present.
3. Update `products.status='approved_for_listing'`.

## 3. Approve a Listing
1. Inspect `listing_metadata` row for the product.
2. Verify required disclosures are present in the description.
3. Verify hero image clearly says "DIGITAL PLANS".
4. Update `listing_metadata.approval_status='approved'`.
5. Cron picks it up; the publish workflow re-runs compliance and creates
   the Etsy draft listing. **Etsy publication still requires you to flip the
   listing live in Etsy seller tools** (Phase 3 may automate this; review then).

## 4. Handle a Customer Message
1. Paste the message and buyer id into the operator UI / CLI.
2. Workflow logs a row in `customer_messages` with intent + risk + draft.
3. If `risk_level='low'`, glance and send.
4. Otherwise, edit the draft, then mark `approval_status='approved'`.
5. Send via Etsy seller tools (Etsy messaging endpoints are not used until
   that endpoint is approved by Etsy for our app).

## 5. Update Digital Files
1. Update source files in `/products/[slug]/source/`.
2. Bump version in `metadata/listing.json`.
3. Add changelog entry in `metadata/changelog.md`.
4. Generate fresh PDFs into `/exports/pdf/`.
5. Re-run compliance via `npm run agent:compliance`.
6. Operator updates the file in Etsy listing tools (Etsy's Open API does
   support file association — Phase 3 wraps this).

## 6. Pause Automation
- Set `EMERGENCY_STOP=true` in your hosting env, or
- Run `npm run emergency-stop` for a local sentinel, or
- Disable the n8n workflow.
- Document the reason in a new compliance_log row with `event_type='override'`.

## 7. Rotate Credentials
See the runbook in [docs/13_security.md](13_security.md).

## 8. Read Weekly Reports
- Reports stored in `weekly_reports`; latest also rendered in
  `reports/generated/[date].md` if the operator UI is enabled.
- Look at: revenue, top products, failed automations, compliance flags,
  recommendations. Act on flagged recommendations before next week.

## 9. Common Customer Issues
| Issue | Recommended path |
|-------|------------------|
| "I can't find the download" | Send the canned download-help reply (low risk). |
| "The materials list is unclear" | Edit the draft reply for the specific section; add the question to the improvement loop. |
| "I want a refund" | Always treat as HIGH risk. Review the Etsy case before responding. |
| "Will it survive my snow load?" | Decline to give a specific answer; refer to local builder/engineer; do not promise. |
| "Can you customize this?" | We do not offer custom design. Recommend closest existing product. |

## 10. Avoid Etsy Policy Problems
- Always run Compliance Agent before approving a listing.
- Always disclose AI assistance if it materially shapes buyer-facing content.
- Never copy descriptions or images from competitors.
- Never solicit reviews in exchange for anything.
- Never move transactions off Etsy.
