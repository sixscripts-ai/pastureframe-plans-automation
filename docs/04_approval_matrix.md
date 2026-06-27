# 04 — Human Approval Matrix

| Action                                   | Automation may | Human approval required |
|------------------------------------------|:--------------:|:-----------------------:|
| Draft product copy / materials / FAQ     |      Yes       |           No            |
| Draft listing title, tags, description   |      Yes       |           No            |
| Generate image briefs                    |      Yes       |           No            |
| Classify a customer message              |      Yes       |           No            |
| Draft a low-risk customer reply          |      Yes       |           No            |
| Sync orders/receipts (read-only)         |      Yes       |           No            |
| Generate weekly report                   |      Yes       |           No            |
| Log compliance flags                     |      Yes       |           No            |
| **Publish a new listing**                |       —        |        **Yes**          |
| **Edit a live listing**                  |       —        |        **Yes**          |
| **Change a price**                       |       —        |        **Yes**          |
| **Upload revised buyer-facing files**    |       —        |        **Yes**          |
| **Send medium/high-risk customer reply** |       —        |        **Yes**          |
| **Issue a refund**                       |       —        |        **Yes**          |
| **Offer major discounts (>10%)**         |       —        |        **Yes**          |
| **Change shop policies**                 |       —        |        **Yes**          |
| **Post to external social media**        |       —        |        **Yes**          |
| **Make legal/tax/engineering claims**    |       —        |        **Yes (legal)**  |

## Risk Tiers (Customer Messages)
- **Low:** Download help, factual product clarification, "thanks" replies.
  Auto-draft, send after light human glance OR auto-send if explicitly
  approved per template.
- **Medium:** Materials questions requiring specifics, build advice,
  shipping confusion, mild complaints. Always human-approve.
- **High:** Refund demands, safety/injury reports, animal-harm claims,
  legal threats, harassment, custom-engineering requests, anything alleging
  defect or risk. Always human-approve. Never auto-send.

## Implementation Pointers
- See [src/agents/customer_service.ts](../src/agents/customer_service.ts) for
  classification + risk scoring.
- See [database/schema.sql](../database/schema.sql) `customer_messages.approval_required`.
- See [src/workflows/publish_listing.ts](../src/workflows/publish_listing.ts) for
  the gated publish flow.
