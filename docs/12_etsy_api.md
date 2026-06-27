# 12 — Etsy API Integration Plan

Reference: https://developer.etsy.com/documentation/

## OAuth 2.0 (Authorization Code + PKCE)
- Developer app name: **PastureFrame Plans Automation**.
- Development redirect URI: `http://localhost:3000/api/etsy/callback`.
- Production redirect URI: `https://pastureframeplans.com/api/etsy/callback`
  unless the final domain changes.
- Required scopes (least privilege):
  `listings_r listings_w shops_r shops_w transactions_r`.
- Do not request `transactions_w` until the system actually performs
  fulfillment/write actions.
- Add `email_r` only after Commercial Access is granted (we are personal-access).
- Tokens are stored in environment / secret manager and refreshed by
  [src/api/etsy/oauth.ts](../src/api/etsy/oauth.ts).
- Run `npm run etsy:auth` to perform the initial dance from the CLI.

## Per-request Headers
- `x-api-key: <keystring>:<shared_secret>` — required on every request.
- `Authorization: Bearer <access_token>` — required on scoped endpoints.

## Endpoints We Use
| Purpose | HTTP | Path | Scope |
|---------|------|------|-------|
| Heartbeat (avoid dormancy ban) | GET | `/shops/{shop_id}` | `shops_r` |
| Create draft listing | POST | `/shops/{shop_id}/listings` | `listings_w` |
| Set type=download | PATCH | `/shops/{shop_id}/listings/{listing_id}` | `listings_w` |
| Receipts | GET | `/shops/{shop_id}/receipts` | `transactions_r` |
| Taxonomy nodes | GET | `/seller-taxonomy/nodes` | none (public) |

## Listing Field Recipe (Digital Download)
```ts
{
  quantity: 999,
  title: "<= 140 chars",
  description: "...with required disclosures",
  price: 39,
  who_made: "i_did",
  when_made: "made_to_order",
  taxonomy_id: <discovered>,
  tags: ["<= 13 tags, each <= 20 chars"],
  type: "download"
}
```

## Reliability
- Retry 5xx and 429 with exponential backoff and `Retry-After` honor; max 5
  attempts. See [src/lib/retry.ts](../src/lib/retry.ts).
- 4xx errors are NOT retried; surfaced to the operator.
- Daily heartbeat job calls `getShop` to keep the app from being marked
  dormant after 6 months.

## Mutation Safety
- Every mutating request requires `mutating: true` in our wrapper; this
  triggers `EMERGENCY_STOP` checks.
- Keep `ALLOW_AUTO_PUBLISH=false`; the app may draft listings and reports, but
  Ashton approves publishing, price changes, policy changes, file uploads, and
  customer messages.
- Publishing a listing requires an `approval_status='approved'` row in
  `listing_metadata` AND a passing last-mile compliance check before the
  Etsy call is made.
