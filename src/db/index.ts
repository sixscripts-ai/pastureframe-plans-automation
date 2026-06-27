import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { env } from '../config.js';

let _client: SupabaseClient | null = null;

export function db(): SupabaseClient {
  if (_client) return _client;
  if (!env.SUPABASE_URL || !env.SUPABASE_SERVICE_ROLE_KEY) {
    throw new Error('Supabase not configured: set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY');
  }
  _client = createClient(env.SUPABASE_URL, env.SUPABASE_SERVICE_ROLE_KEY, {
    auth: { persistSession: false },
  });
  return _client;
}

export async function logAutomationRun(input: {
  workflow_name: string;
  trigger: 'manual' | 'cron' | 'webhook' | 'agent_chain';
  input_summary?: string;
  output_summary?: string;
  success: boolean;
  error_message?: string;
  duration_ms?: number;
}): Promise<void> {
  try {
    await db().from('automation_runs').insert(input);
  } catch {
    // best-effort; never crash a workflow because logging failed
  }
}

export async function logCompliance(input: {
  event_type: 'block' | 'warn' | 'pass' | 'override' | 'policy_review' | 'disclosure';
  source_policy?: string;
  system_area?: string;
  issue: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  action_taken?: string;
  approval_by?: string;
  related_id?: string;
}): Promise<void> {
  try {
    await db().from('compliance_log').insert(input);
  } catch {
    /* best-effort */
  }
}
