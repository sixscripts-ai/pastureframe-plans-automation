import { callLLM } from '../lib/llm.js';
import type { AgentEnvelope } from './types.js';

/** Agent 2 — Product Development Agent. Drafts the package for one product. */
export interface ProductDevInput {
  product_type: string;
  product_name: string;
  specifications: string[];
  optional_features?: string[];
}

export interface ProductPackage {
  outline: string;
  materials_list: string[];
  cut_list: string[];
  guide_structure: string[];
  image_prompts: string[];
  improvement_recommendations: string[];
}

const SYSTEM = `You are a senior product designer for DIY homestead and farm structures.
You design plans that are practical, buildable, and conservatively spec'd.
You NEVER claim engineering, stamped, code-approved, snow/wind/seismic load
ratings, or veterinary/medical guarantees. You always include a buyer-side
DIY disclaimer about local codes, climate, predators, and animal care.
Return strict JSON matching the requested schema.`;

export async function draftProductPackage(
  input: ProductDevInput,
): Promise<AgentEnvelope<ProductPackage>> {
  const user = `Design a digital DIY plan package.

PRODUCT: ${input.product_name}
TYPE: ${input.product_type}
SPECIFICATIONS:
${input.specifications.map((s) => '- ' + s).join('\n')}
${
  input.optional_features?.length
    ? 'OPTIONAL FEATURES:\n' + input.optional_features.map((s) => '- ' + s).join('\n')
    : ''
}

Return JSON:
{
  "outline": "<overview paragraph>",
  "materials_list": ["..."],
  "cut_list": ["..."],
  "guide_structure": ["Section 1: ...", "Section 2: ..."],
  "image_prompts": ["8-10 SDXL-style prompts for original renders"],
  "improvement_recommendations": ["..."]
}`;

  const r = await callLLM<ProductPackage>({ system: SYSTEM, user, responseFormat: 'json' });
  const out = r.json ?? {
    outline: r.text,
    materials_list: [],
    cut_list: [],
    guide_structure: [],
    image_prompts: [],
    improvement_recommendations: [],
  };
  return {
    output: out,
    confidence: r.json ? 'medium' : 'low',
    assumptions: [
      'Material grades (PT 4x4, 2x4 SPF, 1/2" hardware cloth) are typical North American defaults.',
      'Dimensions reflect input specs; verify before publishing.',
    ],
    compliance_concerns: [],
    human_review_required: true,
    suggested_next_action: 'Operator reviews outline + materials, then runs Listing Agent.',
  };
}
