# 10 — Agent Architecture

Each agent lives under [src/agents/](../src/agents). All agents return the
shared `AgentEnvelope<T>` defined in [src/agents/types.ts](../src/agents/types.ts):

```ts
{
  output: T,
  confidence: 'low' | 'medium' | 'high',
  assumptions: string[],
  compliance_concerns: string[],
  human_review_required: boolean,
  suggested_next_action: string,
}
```

| # | Agent | File | Side effects | Approval gate |
|---|-------|------|--------------|---------------|
| 1 | Compliance | [src/agents/compliance.ts](../src/agents/compliance.ts) | Logs to `compliance_log` | Blocks on `pass=false` |
| 2 | Product Development | [src/agents/product_dev.ts](../src/agents/product_dev.ts) | None | Always require human review |
| 3 | Etsy Listing | [src/agents/listing.ts](../src/agents/listing.ts) | None | Always require human review |
| 4 | Customer Service | [src/agents/customer_service.ts](../src/agents/customer_service.ts) | None | Auto-flag any non-low risk |
| 5 | Order Operations | [src/agents/orders.ts](../src/agents/orders.ts) | Inserts into `orders` (read-only sync) | n/a (read-only) |
| 6 | Marketing | [src/agents/marketing.ts](../src/agents/marketing.ts) | None | Drafts only — operator publishes |
| 7 | Analytics | [src/agents/analytics.ts](../src/agents/analytics.ts) | Upserts `weekly_reports` | n/a |
| 8 | Admin | [src/agents/admin.ts](../src/agents/admin.ts) | Logs warnings | n/a |

## Why static rules in Compliance Agent?
LLM-only compliance is non-deterministic. We layer LLM nuance on top of a
deterministic rule set so that an LLM regression cannot accidentally pass a
listing that says "engineer approved". See
[src/agents/compliance.ts](../src/agents/compliance.ts) for the rule list.

## Risk-rating override in Customer Service
The LLM may classify a refund request as "low" risk; we explicitly override
to "high" for a fixed list of intents. See `HIGH_RISK` and `MEDIUM_RISK` in
[src/agents/customer_service.ts](../src/agents/customer_service.ts).
