# Compliance Working Folder

This directory holds compliance artifacts that supplement the live
`compliance_log` table:

- `etsy-policy-snapshots/` — periodically saved snapshots of relevant
  Etsy policy pages (Seller Policy, Prohibited Items, IP Policy) with the
  date pulled, so we can prove what the policy said when we acted.
- `disclaimer-library.md` — canonical disclaimer text used in PDFs and
  listings. Source of truth for the "DIY / verify locally" language.
- `decisions/` — one markdown file per decision where we deviated from a
  default rule with reasoning and approver.

Re-snapshot Etsy's policy pages quarterly and immediately before any major
release.
