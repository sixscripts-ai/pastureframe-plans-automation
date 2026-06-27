# n8n Workflows

This directory holds the exported JSON for n8n flows. Each flow is a thin
wrapper that calls our Cloudflare Worker route or an `npx tsx src/cli/...`
command on the host.

## Flow 1 — Order Sync (cron, hourly)
- **Trigger:** Cron `0 * * * *`.
- **Action:** HTTP POST to `${API_BASE}/workflows/order-sync` (Worker route)
  OR shell exec `tsx src/cli/run-agent.ts orders` if running n8n on the same host.
- **Notification on failure:** Slack webhook (`SLACK_WEBHOOK_URL`).

## Flow 2 — Weekly Report (cron, Mon 08:00)
- **Trigger:** Cron `0 8 * * 1`.
- **Action:** Shell exec `npm run report:weekly`.
- **Notification on success:** Email to `NOTIFY_EMAIL` with the report JSON.

## Flow 3 — Heartbeat (cron, daily)
- **Trigger:** Cron `0 12 * * *`.
- **Action:** GET `${API_BASE}/heartbeat` (calls `etsy.heartbeat()`) so the
  Etsy app is not flagged dormant after 6 months.

## Flow 4 — Approval Notifier (event)
- **Trigger:** Supabase webhook on `listing_metadata` insert.
- **Action:** Email/Slack the listing summary + a link to approve.

> JSON exports are committed once n8n is set up. Until then this README
> documents the spec.
