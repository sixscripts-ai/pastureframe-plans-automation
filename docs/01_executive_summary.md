# 01 — Executive Summary

## Project
PastureFrame Plans Automation — a semi-automated, compliance-first operating
system for Ashton Aschenbrener's Etsy shop selling **digital downloadable**
mobile coop and homestead structure plans.

## Goal
Help Ashton produce, list, sell, support, and improve the chicken coop flagship
first, then expand into related digital plan products while keeping clear human
control over every action that publishes content, moves money, or contacts a
buyer.

## What This System Does (Automated)
- Drafts product packages (copy, materials, cut lists, image briefs, FAQ).
- Drafts Etsy listings (title, tags, description, image plan, taxonomy).
- Classifies inbound customer messages by intent and risk.
- Drafts customer responses with risk labels.
- Syncs Etsy orders/receipts via Open API v3.
- Generates weekly reports (revenue, orders, top products, issues).
- Logs every automation run, every compliance flag, every approval decision.

## What This System Does NOT Do (Human-Gated)
- Publish or edit live listings.
- Change prices or issue refunds.
- Send buyer-facing messages tagged medium/high risk.
- Post to external social media.
- Make engineering, safety, animal-care, tax, or legal claims without review.

## Recommended Stack (Final)
- **Language/Runtime:** TypeScript + Node 20.
- **Database:** Supabase (Postgres + Row-Level Security + Storage).
- **File storage:** Google Drive for working files; Supabase Storage for
  buyer-facing PDFs (mirrored to Etsy listing's digital file slot).
- **Automation glue:** n8n (self-hosted) for cron + webhook orchestration.
- **LLM:** Anthropic Claude (primary) with OpenAI fallback.
- **Image templates:** Canva Pro (manual) + Figma library (source of truth).
- **Hosting:** Cloudflare Workers (lightweight API) + Supabase Edge Functions.
- **Repo:** GitHub, single mono-repo.

## Phase Plan
1. **Phase 1 (now):** Manual-first foundation — repo, schema, two flagship
   product packages, listing drafts, manual upload checklist.
2. **Phase 2:** Semi-automated drafting + approval UI.
3. **Phase 3:** Etsy Open API v3 — OAuth, draft listing creation, order sync.
4. **Phase 4:** Marketing engine drafts (Pinterest, blog, IG, email).
5. **Phase 5:** Scaling — additional products, bundles, improvement loop.

## Acceptance Status
See [docs/19_launch_checklist.md](19_launch_checklist.md) for the live
acceptance checklist. Phase 1 deliverables are scaffolded in this commit.
