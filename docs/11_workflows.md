# 11 — Automation Workflows

| # | Workflow | Trigger | Side effect | File |
|---|----------|---------|-------------|------|
| 1 | New Product Creation | Manual / DB row | None (drafts only) | [src/workflows/new_product.ts](../src/workflows/new_product.ts) |
| 2 | Listing Draft Creation | After human approval | Etsy API write (gated) | [src/workflows/publish_listing.ts](../src/workflows/publish_listing.ts) |
| 3 | Order Sync | Cron (hourly) | Insert into `orders` | [src/workflows/order_sync.ts](../src/workflows/order_sync.ts) |
| 4 | Customer Message Intake | Manual paste / future webhook | Insert into `customer_messages` | [src/workflows/message_intake.ts](../src/workflows/message_intake.ts) |
| 5 | Weekly Report | Cron (Mon 08:00) | Upsert `weekly_reports` | [src/workflows/weekly_report.ts](../src/workflows/weekly_report.ts) |
| 6 | Product Improvement Loop | Cron (weekly) or manual | None (drafts only) | [src/workflows/improvement_loop.ts](../src/workflows/improvement_loop.ts) |

## n8n Hookup
See [automations/n8n/README.md](../automations/n8n/README.md) for the cron and
webhook shells. Workflows call the corresponding `tsx src/cli/...` entrypoint
or POST to the Cloudflare Worker route.

## Hard Rules
- Every mutating Etsy call passes through `etsyRequest({ ..., mutating: true })`
  which respects `EMERGENCY_STOP`.
- Every workflow logs to `automation_runs`.
- Every compliance failure logs to `compliance_log` with severity.
- No workflow may auto-publish, auto-refund, or auto-send a non-low-risk
  customer message.
