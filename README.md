# PastureFrame Plans Automation

A semi-automated, compliance-first Etsy operating system for **PastureFrame
Plans**, Ashton Aschenbrener's shop selling **digital downloadable** mobile coop
and homestead structure plans. Automation drafts, classifies, summarizes, and recommends.
**Humans approve everything that publishes, charges, refunds, or messages buyers.**

## Status
Phase 1 — Chicken coop flagship foundation scaffolded.

## Quick Links
- [Executive Summary](docs/01_executive_summary.md)
- [Compliance Research Memo](docs/02_compliance_memo.md)
- [System Architecture](docs/03_architecture.md)
- [Etsy Store Setup Package](docs/05_store_setup.md)
- [Brand Identity Package](docs/06_brand_identity.md)
- [Initial Product Catalog](docs/07_product_catalog.md)
- [Database Schema](database/schema.sql)
- [Agent Architecture](docs/10_agents.md)
- [Automation Workflows](docs/11_workflows.md)
- [Etsy API Integration Plan](docs/12_etsy_api.md)
- [Security Plan](docs/13_security.md)
- [Listing Templates](templates/listings/listing_template.md)
- [Image Template System](docs/15_image_templates.md)
- [MVP Roadmap](docs/16_roadmap.md)
- [Testing Plan](docs/17_testing_plan.md)
- [Operating Manual](docs/18_operating_manual.md)
- [Launch Checklist](docs/19_launch_checklist.md)
- [30-Day Growth Plan](docs/20_growth_plan.md)

## Setup
```bash
cp .env.example .env
# Fill in values
npm install
npm run typecheck
npm test
```

## Approval Gates
Nothing in this system publishes a listing, edits a live listing, changes a
price, sends a sensitive customer message, issues a refund, or posts to social
media without explicit human approval. See [docs/04_approval_matrix.md](docs/04_approval_matrix.md).

## Disclaimer
This repository's content (plans, drawings, copy, lists) is DIY educational
material. Buyers must verify local codes, climate loads, predator pressure, and
animal-care requirements for their site. The seller does not provide stamped
engineering or permitting approval.
