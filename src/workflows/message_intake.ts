import { classifyAndDraft } from '../agents/customer_service.js';
import { db, logAutomationRun } from '../db/index.js';
import { hashBuyerId } from '../lib/hash.js';
import { redactPII } from '../lib/redact.js';

/**
 * Workflow 4 — Customer Message Intake.
 * Currently invoked by the operator pasting a message + buyer id. When Etsy's
 * messages endpoint is granted, swap the trigger here.
 */
export interface MessageIntakeInput {
  buyer_user_id: string | number;
  order_id?: string;
  raw_message: string;
}

export async function messageIntakeWorkflow(input: MessageIntakeInput): Promise<{
  classification: Awaited<ReturnType<typeof classifyAndDraft>>;
  message_id: string | null;
}> {
  const t0 = Date.now();
  const classification = await classifyAndDraft(input.raw_message);

  const supa = db();
  const insert = await supa
    .from('customer_messages')
    .insert({
      order_id: input.order_id ?? null,
      buyer_id_hash: hashBuyerId(input.buyer_user_id),
      message_text_redacted: redactPII(input.raw_message),
      detected_intent: classification.output.intent,
      sentiment: classification.output.sentiment,
      risk_level: classification.output.risk_level,
      suggested_response: classification.output.suggested_response,
      approval_required: classification.output.risk_level !== 'low',
    })
    .select('message_id')
    .single();

  await logAutomationRun({
    workflow_name: 'message_intake',
    trigger: 'manual',
    input_summary: `intent=${classification.output.intent} risk=${classification.output.risk_level}`,
    output_summary: insert.error ? insert.error.message : `msg=${insert.data?.message_id}`,
    success: !insert.error,
    duration_ms: Date.now() - t0,
  });

  return { classification, message_id: insert.data?.message_id ?? null };
}
