# 03 — System Architecture

```
                      ┌──────────────────────────────────────┐
                      │            Ashton (operator)          │
                      │   Reviews / Approves / Publishes      │
                      └───────────────┬──────────────────────┘
                                      │ approval gates
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
   ┌────▼─────┐  ┌──────────┐  ┌──────▼──────┐  ┌────────────┐ ┌────▼─────┐
   │ Approval │  │  n8n     │  │ Cloudflare  │  │  Supabase  │ │  Google  │
   │   UI     │◀▶│ workflows│◀▶│  Worker API │◀▶│  Postgres  │ │   Drive  │
   │ (Phase 2)│  │ (cron +  │  │  (REST)     │  │  + Storage │ │ (working │
   │          │  │ webhooks)│  │             │  │            │ │  files)  │
   └────┬─────┘  └────┬─────┘  └────┬────────┘  └────────────┘ └──────────┘
        │             │             │                ▲
        │             │             │                │ logs / state
        │             ▼             ▼                │
        │     ┌────────────────────────────────────┐ │
        │     │             Agents (TS)            │ │
        │     │  Compliance · Product · Listing ·  │─┘
        │     │  CustomerSvc · Orders · Marketing ·│
        │     │  Analytics · Admin                 │
        │     └────────────┬───────────────────────┘
        │                  │
        │            ┌─────▼──────┐
        │            │ LLM Router │  (Anthropic primary, OpenAI fallback)
        │            └─────┬──────┘
        │                  │
        │            ┌─────▼──────────┐
        └───────────▶│  Etsy Open API │  (OAuth 2.0 + PKCE, listings/transactions)
                     │       v3       │
                     └────────────────┘
```

## Layers
1. **Operator surface:** Approval UI (Phase 2) + email/Slack notifications.
2. **Orchestration:** n8n flows trigger agents on cron or events.
3. **API edge:** Cloudflare Worker exposes a small REST surface for the UI
   and webhook receivers.
4. **Domain:** Pure-TypeScript agents in [src/agents/](../src/agents).
5. **Data:** Supabase Postgres with RLS; Supabase Storage for buyer-facing
   PDFs; Google Drive for working source files.
6. **External:** Etsy Open API v3, Anthropic, OpenAI.

## Module Boundaries
- `src/agents/*` — pure functions; no I/O except via injected ports.
- `src/api/etsy/*` — Etsy client + OAuth, the only place that talks to Etsy.
- `src/db/*` — Supabase access, the only place that talks to Postgres.
- `src/lib/*` — utilities (redaction, hashing, retry, logger).
- `src/workflows/*` — agent compositions used by CLI and n8n.
- `src/cli/*` — CLI entrypoints used by n8n / cron / humans.

## Approval Flow (Generic)
1. An agent generates a draft and writes it to the relevant table with
   `approval_status = 'pending'` and `risk_level` set.
2. Notifier emits an email/Slack message with a link to the draft.
3. Human reviews, edits if needed, and clicks Approve (Phase 2 UI) or
   updates the row directly (Phase 1).
4. A webhook/cron job picks up rows where
   `approval_status = 'approved' AND published_at IS NULL` and performs the
   side effect (Etsy publish, message send, refund, etc.).
5. All steps logged in `automation_runs` and `compliance_log`.

## Failure Posture
- Every agent run logs to `automation_runs` with success/error.
- Etsy 4xx → no retry, surface to operator.
- Etsy 5xx / 429 → exponential backoff, max 5 attempts, respect `Retry-After`.
- LLM failures → fall through to fallback provider once, then surface.
- `EMERGENCY_STOP=true` env var halts all side-effecting operations.
