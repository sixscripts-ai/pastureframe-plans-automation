import { callLLM } from '../lib/llm.js';
import type { AgentEnvelope } from './types.js';

/** Agent 3 — Etsy Listing Agent. */
export interface ListingInput {
  product_name: string;
  product_type: string;
  target_customer: string;
  features: string[];
  price: number;
}

export interface ListingDraft {
  seo_title: string;        // <= 140 chars
  description: string;       // includes mandatory disclaimers
  tags: string[];           // <= 13, each <= 20 chars
  whats_included: string[];
  who_this_is_for: string[];
  who_this_is_not_for: string[];
  materials_preview: string[];
  tools_preview: string[];
  faq: { q: string; a: string }[];
  image_concepts: string[]; // 8-10
  pdf_table_of_contents: string[];
  upsell_bundle_suggestions: string[];
  price_recommendation: number;
  launch_priority_score: number; // 1-10
}

const SYSTEM = `You are an Etsy listing copywriter for digital DIY homestead plans.
Hard rules:
- The product is a DIGITAL DOWNLOAD. Description must say "no physical product
  will be shipped" and "buyer receives plan files only".
- Personal use only — no resale, redistribution, sharing, or claiming as original work.
- Include the standard DIY disclaimer about local codes, climate, predators, and animal care.
- NO engineering, stamped, code-approved, or load-rating claims.
- Tags: 13 max, each <= 20 chars, lowercase preferred, no special characters.
- Title <= 140 chars.
Return strict JSON.`;

export async function draftListing(input: ListingInput): Promise<AgentEnvelope<ListingDraft>> {
  const user = `Draft an Etsy listing for "${input.product_name}" (${input.product_type}).
Target customer: ${input.target_customer}
Suggested price: $${input.price}
Key features:
${input.features.map((f) => '- ' + f).join('\n')}

Return JSON with these fields:
seo_title, description, tags (array), whats_included (array),
who_this_is_for (array), who_this_is_not_for (array), materials_preview (array),
tools_preview (array), faq (array of {q,a}), image_concepts (8-10 strings),
pdf_table_of_contents (array), upsell_bundle_suggestions (array),
price_recommendation (number), launch_priority_score (1-10).`;

  const r = await callLLM<ListingDraft>({ system: SYSTEM, user, responseFormat: 'json' });
  const out = r.json;
  if (!out) {
    return {
      output: {} as ListingDraft,
      confidence: 'low',
      assumptions: [],
      compliance_concerns: ['LLM did not return JSON; rerun.'],
      human_review_required: true,
      suggested_next_action: 'Re-run draftListing with stricter prompt.',
    };
  }

  // Hard validations.
  const concerns: string[] = [];
  if (out.seo_title && out.seo_title.length > 140) concerns.push('Title exceeds 140 chars.');
  if (out.tags) {
    if (out.tags.length > 13) concerns.push('More than 13 tags.');
    if (out.tags.some((t) => t.length > 20)) concerns.push('A tag exceeds 20 chars.');
  }
  if (out.description && !/digital download/i.test(out.description)) {
    concerns.push('Description missing "digital download" statement.');
  }
  if (out.description && !/personal use/i.test(out.description)) {
    concerns.push('Description missing personal-use license statement.');
  }
  if (out.description && !/local code|local codes|verify/i.test(out.description)) {
    concerns.push('Description missing DIY/local-codes disclaimer.');
  }

  return {
    output: out,
    confidence: concerns.length === 0 ? 'high' : 'medium',
    assumptions: ['Etsy taxonomy_id will be selected at publish time via getSellerTaxonomyNodes.'],
    compliance_concerns: concerns,
    human_review_required: true,
    suggested_next_action: concerns.length
      ? 'Edit listing to address compliance concerns.'
      : 'Run Compliance Agent then queue for human approval.',
  };
}
