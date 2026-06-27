# 17 — Testing Plan

| # | Test | Type | Status / File |
|---|------|------|---------------|
| 1 | OAuth code exchange happy path | unit/integration | _pending — needs sandbox creds_ |
| 2 | Listing draft creation | integration (sandbox) | _pending_ |
| 3 | Product metadata generation | unit | tested via agent JSON envelope shape |
| 4 | Order sync | integration | _pending_ |
| 5 | Duplicate order prevention | unit | covered by `upsert(... ignoreDuplicates)` |
| 6 | Customer message classification | unit | manual fixture set in [tests/](../tests) |
| 7 | Approval gates | unit | publish workflow refuses without `approval_status='approved'` |
| 8 | Compliance blocking | unit | [tests/compliance.test.ts](../tests/compliance.test.ts) |
| 9 | Failed API recovery | unit | retry helper tested implicitly |
| 10 | Token expiration / refresh | integration | _pending — needs sandbox creds_ |
| 11 | Emergency stop | unit | [tests/emergency_stop.test.ts](../tests/emergency_stop.test.ts) |
| 12 | Weekly report generation | unit/integration | `generateWeeklyReport` returns shape |
| 13 | Data backup | runbook | quarterly Supabase export |

## Run Tests
```bash
npm test
npm run typecheck
```

## Coverage Targets
- Compliance agent rule set: 100% branch coverage.
- Redaction + hash helpers: 100% line coverage.
- Etsy client retry/backoff: scenario tests for 429, 500, 4xx.
