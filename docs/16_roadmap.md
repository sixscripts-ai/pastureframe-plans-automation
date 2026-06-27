# 16 — MVP Roadmap

## Phase 1 — Manual-First Foundation (in progress)
- [x] Repo scaffolded.
- [x] Compliance memo and architecture written.
- [x] Database schema authored.
- [x] 8 agents and 6 workflows implemented.
- [x] First two flagship product packages drafted (Mobile Coop, Garden Shade Roof).
- [x] Listing template, image template brief, prompts.
- [ ] Original CAD drawings and listing images (Ashton).
- [ ] Etsy account fully configured.

## Phase 2 — Semi-Automated Operations
- [ ] Operator approval UI on Cloudflare Worker (or Supabase Studio views).
- [ ] n8n cron for weekly report and order sync.
- [ ] Email/Slack notifier for pending approvals.
- [ ] Customer message intake from operator clipboard / paste UI.

## Phase 3 — Etsy API Integration
- [ ] OAuth flow live and tokens persisted.
- [ ] `createDraftListing` end-to-end test on a single approved product.
- [ ] Order sync running on cron.
- [ ] Heartbeat job to avoid dormancy.
- [ ] Token expiry alert (< 7 days).

## Phase 4 — Marketing Engine
- [ ] Pinterest pin drafts per listing.
- [ ] Blog outline drafts.
- [ ] Instagram caption drafts.
- [ ] SEO testing tracker (a/b alternative titles per listing).

## Phase 5 — Scaling
- [ ] Add 6 more products from the catalog.
- [ ] Seasonal bundles.
- [ ] Improvement loop reviewing every 10 sales per product.
- [ ] Analytics-driven roadmap.
