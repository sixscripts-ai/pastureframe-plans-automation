import { db } from '../db/index.js';
import { logger } from '../lib/logger.js';
import type { AgentEnvelope } from './types.js';

/** Agent 8 — Admin Agent. Maintains docs, logs, and credential alerts. */
export interface AdminCheck {
  etsy_token_days_remaining: number | null;
  failed_runs_24h: number;
  open_compliance_flags_high: number;
  pending_listing_approvals: number;
  pending_high_risk_messages: number;
}

export async function runAdminCheck(): Promise<AgentEnvelope<AdminCheck>> {
  const supa = db();
  const since = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();

  const [failed, flags, listings, messages] = await Promise.all([
    supa
      .from('automation_runs')
      .select('run_id', { count: 'exact', head: true })
      .eq('success', false)
      .gte('timestamp', since),
    supa
      .from('compliance_log')
      .select('log_id', { count: 'exact', head: true })
      .eq('severity', 'high'),
    supa
      .from('listing_metadata')
      .select('listing_id', { count: 'exact', head: true })
      .eq('approval_status', 'pending'),
    supa
      .from('customer_messages')
      .select('message_id', { count: 'exact', head: true })
      .eq('approval_status', 'pending')
      .in('risk_level', ['medium', 'high']),
  ]);

  let etsy_token_days_remaining: number | null = null;
  const exp = process.env.ETSY_TOKEN_EXPIRES_AT;
  if (exp) {
    const ms = Number(exp) * 1000 - Date.now();
    etsy_token_days_remaining = Math.floor(ms / (1000 * 60 * 60 * 24));
  }

  const out: AdminCheck = {
    etsy_token_days_remaining,
    failed_runs_24h: failed.count ?? 0,
    open_compliance_flags_high: flags.count ?? 0,
    pending_listing_approvals: listings.count ?? 0,
    pending_high_risk_messages: messages.count ?? 0,
  };

  logger.info(out, 'admin.check.ok');

  const concerns: string[] = [];
  if (etsy_token_days_remaining !== null && etsy_token_days_remaining < 7)
    concerns.push('Etsy refresh token expires in <7 days.');
  if (out.failed_runs_24h > 0) concerns.push('Failed automation runs in last 24h.');
  if (out.open_compliance_flags_high > 0) concerns.push('Open high-severity compliance flags.');

  return {
    output: out,
    confidence: 'high',
    assumptions: [],
    compliance_concerns: concerns,
    human_review_required: concerns.length > 0,
    suggested_next_action: concerns.length ? 'Address concerns above.' : 'No action needed.',
  };
}
