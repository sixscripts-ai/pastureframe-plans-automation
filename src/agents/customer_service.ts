import { callLLM } from '../lib/llm.js';
import { redactPII } from '../lib/redact.js';
import type { AgentEnvelope } from './types.js';

/** Agent 4 — Customer Service Agent. */
export type MessageIntent =
  | 'download_help'
  | 'product_clarification'
  | 'materials_question'
  | 'refund_request'
  | 'complaint'
  | 'safety_concern'
  | 'custom_design'
  | 'legal_threat'
  | 'harassment_spam'
  | 'positive_feedback'
  | 'review_issue'
  | 'other';

export interface MessageClassification {
  intent: MessageIntent;
  sentiment: 'positive' | 'neutral' | 'negative';
  risk_level: 'low' | 'medium' | 'high';
  suggested_response: string;
}

const HIGH_RISK: MessageIntent[] = [
  'refund_request',
  'safety_concern',
  'legal_threat',
  'harassment_spam',
  'custom_design',
];
const MEDIUM_RISK: MessageIntent[] = ['complaint', 'materials_question', 'review_issue'];

const SYSTEM = `You are an Etsy customer service classifier and drafter for a digital
homestead plans shop. The customer message has been redacted of PII before
reaching you. Classify the intent and draft a polite, factual reply.
Tone: professional, concise, helpful. Never:
- Promise refunds, engineering certifications, or code approvals.
- Admit liability.
- Encourage off-Etsy transactions.
- Solicit reviews in exchange for anything.
Return strict JSON.`;

export async function classifyAndDraft(
  rawMessage: string,
): Promise<AgentEnvelope<MessageClassification>> {
  const redacted = redactPII(rawMessage);
  const user = `Customer message (PII redacted):
"""
${redacted}
"""

Return JSON:
{
  "intent": "download_help|product_clarification|materials_question|refund_request|complaint|safety_concern|custom_design|legal_threat|harassment_spam|positive_feedback|review_issue|other",
  "sentiment": "positive|neutral|negative",
  "risk_level": "low|medium|high",
  "suggested_response": "..."
}`;

  const r = await callLLM<MessageClassification>({
    system: SYSTEM,
    user,
    responseFormat: 'json',
  });
  let out: MessageClassification = r.json ?? {
    intent: 'other',
    sentiment: 'neutral',
    risk_level: 'medium',
    suggested_response: '',
  };

  // Override risk if LLM under-rated something we always treat as high.
  if (HIGH_RISK.includes(out.intent)) out = { ...out, risk_level: 'high' };
  else if (MEDIUM_RISK.includes(out.intent) && out.risk_level === 'low') {
    out = { ...out, risk_level: 'medium' };
  }

  return {
    output: out,
    confidence: r.json ? 'medium' : 'low',
    assumptions: ['Buyer PII has been redacted upstream.'],
    compliance_concerns: [],
    human_review_required: out.risk_level !== 'low',
    suggested_next_action:
      out.risk_level === 'low'
        ? 'Operator quick-glance, then send.'
        : 'Operator must review and approve before sending.',
  };
}
