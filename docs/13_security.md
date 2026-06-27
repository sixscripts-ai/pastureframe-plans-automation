# 13 — Security Plan

## Secrets
- Stored in environment variables and a secret manager (1Password / Doppler / Cloudflare Worker secrets / Supabase Vault).
- **Never** committed to Git. `.env` is in `.gitignore`.
- Rotate on a 90-day schedule and on any suspected leak.
- Access tokens are not logged; pino redaction covers
  `access_token / refresh_token / authorization / x-api-key / buyer_email`.
  See [src/lib/logger.ts](../src/lib/logger.ts).

## Etsy OAuth
- PKCE always. State parameter on every authorize call.
- Store `refresh_token` server-side only.
- Refresh on every request that would use an `access_token` within 60 seconds of expiry. See [src/api/etsy/client.ts](../src/api/etsy/client.ts).

## Buyer Privacy
- Buyer identifiers stored hashed (sha256 + salt) via [src/lib/hash.ts](../src/lib/hash.ts).
- Buyer message text is **redacted** before being sent to any LLM. See [src/lib/redact.ts](../src/lib/redact.ts).
- We do not store raw buyer email unless absolutely required, and only after Etsy commercial-access approval.

## Database
- Supabase service-role key is server-only.
- Phase 2: enable RLS (see [database/migrations/0002_rls.sql](../database/migrations/0002_rls.sql)).
- Backups: enable Supabase point-in-time recovery; export weekly snapshot to private storage.

## Emergency Stop
- `EMERGENCY_STOP=true` env var halts all mutating operations.
- A sentinel file `.emergency_stop` written by `npm run emergency-stop` provides a fast local override.
- Test the stop quarterly.

## Credential Rotation Runbook
1. Generate new Etsy keystring/shared secret in https://www.etsy.com/developers/your-apps.
2. Update secret manager.
3. Run `npm run etsy:auth` to re-issue OAuth tokens.
4. Update Supabase / LLM / Slack secrets in the same manager.
5. Verify `npm run agent:compliance "test"` returns a normal response.
6. Old credentials revoked at the provider.

## Audit Logs
- `automation_runs` — every workflow run, success/failure, duration.
- `compliance_log` — every block/warn with severity.
- All logs retained ≥ 12 months.

## Threat Model (summary)
| Threat | Mitigation |
|--------|-----------|
| Token theft | No token in logs; refresh tokens stored encrypted; HTTPS-only callback. |
| Prompt injection in buyer message | Redact PII; treat LLM output as untrusted; static compliance gate; no auto-actioning of LLM "instructions". |
| Bad LLM output causes bad listing | Static compliance rules + human approval gate. |
| Credential rotation drift | Quarterly rotation runbook + Admin Agent alert when token <7 days from expiry. |
| Etsy API outage | Retry with backoff; queue work; operator visibility via Admin Agent. |
| Insider mistake (publish wrong listing) | Approval row check before Etsy write; emergency stop. |
