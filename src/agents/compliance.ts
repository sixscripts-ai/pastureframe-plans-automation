import { logCompliance } from '../db/index.js';
import type { AgentEnvelope } from './types.js';

/**
 * Agent 1 — Compliance Agent.
 * Static, deterministic checks against our documented compliance rules.
 * (LLM-based checks are layered on later via review() but should never be
 * the only gate — we want this rules engine to be predictable.)
 */

export interface ComplianceInput {
  surface: 'listing' | 'plan_copy' | 'image' | 'message';
  text: string;
  has_digital_only_disclosure?: boolean;
  has_personal_use_license?: boolean;
  has_diy_disclaimer?: boolean;
  has_ai_disclosure?: boolean;
  hero_image_says_digital_plans?: boolean;
}

export interface ComplianceResult {
  pass: boolean;
  blocks: string[];
  warnings: string[];
}

const RISKY_PHRASES: Array<{ pattern: RegExp; reason: string; severity: 'high' | 'medium' }> = [
  { pattern: /\bengineer(ed|ing) approved\b/i, reason: 'Implies engineering certification.', severity: 'high' },
  { pattern: /\bstamped\b/i, reason: 'Implies stamped engineering.', severity: 'high' },
  { pattern: /\bstamped (plans?|drawings?)\b/i, reason: 'Implies stamped engineering.', severity: 'high' },
  { pattern: /\bcode[- ]approved\b/i, reason: 'Implies building-code approval.', severity: 'high' },
  { pattern: /\bguaranteed safe\b/i, reason: 'Unverifiable safety claim.', severity: 'high' },
  { pattern: /\b(snow|wind|seismic) load[- ]rated\b/i, reason: 'Specific load rating without engineering.', severity: 'high' },
  { pattern: /\b(treats|cures|prevents)\b.*\b(disease|illness|infection)\b/i, reason: 'Veterinary medical claim.', severity: 'high' },
  { pattern: /\bguaranteed predator[- ]proof\b/i, reason: 'Unverifiable predator claim.', severity: 'medium' },
  { pattern: /\bphysical (coop|shelter|tractor|roof)\b/i, reason: 'May confuse buyer about physical product.', severity: 'medium' },
  { pattern: /\bship(ping|ped) (in|within)\b/i, reason: 'Digital product is not shipped.', severity: 'medium' },
];

export async function reviewCompliance(input: ComplianceInput): Promise<AgentEnvelope<ComplianceResult>> {
  const blocks: string[] = [];
  const warnings: string[] = [];

  for (const rule of RISKY_PHRASES) {
    if (rule.pattern.test(input.text)) {
      (rule.severity === 'high' ? blocks : warnings).push(rule.reason);
    }
  }

  if (input.surface === 'listing') {
    if (!input.has_digital_only_disclosure) blocks.push('Listing missing "digital download / no physical product" statement.');
    if (!input.has_personal_use_license) blocks.push('Listing missing personal-use license statement.');
    if (!input.has_diy_disclaimer) blocks.push('Listing missing DIY/local-codes disclaimer.');
  }
  if (input.surface === 'image' && input.hero_image_says_digital_plans === false) {
    blocks.push('Hero listing image must clearly say "DIGITAL PLANS".');
  }

  const pass = blocks.length === 0;

  // Persist findings (best-effort).
  for (const issue of blocks) {
    await logCompliance({
      event_type: 'block',
      source_policy: 'internal_rules',
      system_area: input.surface,
      issue,
      severity: 'high',
      action_taken: 'blocked_publish',
    });
  }
  for (const issue of warnings) {
    await logCompliance({
      event_type: 'warn',
      source_policy: 'internal_rules',
      system_area: input.surface,
      issue,
      severity: 'medium',
    });
  }

  return {
    output: { pass, blocks, warnings },
    confidence: 'high',
    assumptions: ['Static rules only — re-run with LLM review for nuanced phrasing.'],
    compliance_concerns: blocks,
    human_review_required: !pass || warnings.length > 0,
    suggested_next_action: pass ? 'Proceed to listing draft.' : 'Fix blocking issues and re-run.',
  };
}
