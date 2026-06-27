import { db } from '../db/index.js';

/**
 * Workflow 6 — Product Improvement Loop.
 * Triggered weekly or after a product reaches 10 sales. Drafts revision
 * notes from customer-message themes; ALWAYS requires human approval before
 * any plan files are updated or republished.
 */
export interface ImprovementInput {
  product_id: string;
}

export interface ImprovementDraft {
  product_id: string;
  notable_questions: string[];
  notable_complaints: string[];
  proposed_revisions: string[];
}

export async function improvementLoop(input: ImprovementInput): Promise<ImprovementDraft> {
  const supa = db();
  const { data: msgs } = await supa
    .from('customer_messages')
    .select('message_text_redacted, detected_intent, risk_level, suggested_response')
    .order('created_at', { ascending: false })
    .limit(50);

  const questions: string[] = [];
  const complaints: string[] = [];
  for (const m of msgs ?? []) {
    if (m.detected_intent === 'product_clarification' || m.detected_intent === 'materials_question') {
      questions.push(m.message_text_redacted);
    } else if (m.detected_intent === 'complaint') {
      complaints.push(m.message_text_redacted);
    }
  }

  return {
    product_id: input.product_id,
    notable_questions: questions.slice(0, 10),
    notable_complaints: complaints.slice(0, 10),
    proposed_revisions: [
      'Operator: review themes and decide which sections to clarify in the next plan revision.',
    ],
  };
}
