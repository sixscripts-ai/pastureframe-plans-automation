import { callLLM } from '../lib/llm.js';
import type { AgentEnvelope } from './types.js';

/** Agent 6 — Marketing Agent. Drafts only; never publishes. */
export interface MarketingInput {
  product_name: string;
  product_url?: string;
  features: string[];
  audience: string;
}

export interface MarketingDrafts {
  pinterest_pins: { title: string; description: string; alt_text: string }[];
  instagram_captions: string[];
  blog_outline: string[];
  email_sequence: { subject: string; body: string }[];
  bundle_recommendations: string[];
}

const SYSTEM = `You write marketing drafts for a small homestead-plans Etsy shop.
Tone: practical, plain-spoken, no hype. Never make engineering, code, safety,
or animal-medical claims. Always indicate digital download. Return strict JSON.`;

export async function draftMarketing(input: MarketingInput): Promise<AgentEnvelope<MarketingDrafts>> {
  const user = `Product: ${input.product_name}
URL: ${input.product_url ?? '(not yet published)'}
Audience: ${input.audience}
Features:
${input.features.map((f) => '- ' + f).join('\n')}

Return JSON: {
  "pinterest_pins":[{"title":"","description":"","alt_text":""}],
  "instagram_captions":[""],
  "blog_outline":[""],
  "email_sequence":[{"subject":"","body":""}],
  "bundle_recommendations":[""]
}`;

  const r = await callLLM<MarketingDrafts>({ system: SYSTEM, user, responseFormat: 'json' });
  return {
    output:
      r.json ?? {
        pinterest_pins: [],
        instagram_captions: [],
        blog_outline: [],
        email_sequence: [],
        bundle_recommendations: [],
      },
    confidence: r.json ? 'medium' : 'low',
    assumptions: ['Drafts must not be posted externally without operator approval.'],
    compliance_concerns: [],
    human_review_required: true,
    suggested_next_action: 'Operator reviews drafts; only operator publishes externally.',
  };
}
