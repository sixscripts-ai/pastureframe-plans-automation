import { db } from '../db/index.js';
import type { AgentEnvelope } from './types.js';

/** Agent 7 — Analytics Agent. Produces a weekly report from Postgres. */
export interface WeeklyReport {
  week_start: string;
  week_end: string;
  revenue: number;
  orders: number;
  top_products: Array<{ product_id: string; orders: number; revenue: number }>;
  customer_messages: number;
  refunds_or_issues: number;
  failed_automations: number;
  compliance_flags: number;
  recommendations: string[];
}

export async function generateWeeklyReport(): Promise<AgentEnvelope<WeeklyReport>> {
  const end = new Date();
  const start = new Date(end.getTime() - 7 * 24 * 60 * 60 * 1000);
  const week_start = start.toISOString().slice(0, 10);
  const week_end = end.toISOString().slice(0, 10);

  const supa = db();
  const [orders, msgs, runs, flags] = await Promise.all([
    supa
      .from('orders')
      .select('order_total, product_ids')
      .gte('purchase_date', start.toISOString())
      .lte('purchase_date', end.toISOString()),
    supa
      .from('customer_messages')
      .select('message_id', { count: 'exact', head: true })
      .gte('created_at', start.toISOString()),
    supa
      .from('automation_runs')
      .select('run_id', { count: 'exact', head: true })
      .eq('success', false)
      .gte('timestamp', start.toISOString()),
    supa
      .from('compliance_log')
      .select('log_id', { count: 'exact', head: true })
      .gte('timestamp', start.toISOString()),
  ]);

  const orderRows = orders.data ?? [];
  const revenue = orderRows.reduce((s, o) => s + Number(o.order_total ?? 0), 0);

  // Top products tally.
  const tally = new Map<string, { orders: number; revenue: number }>();
  for (const o of orderRows) {
    const ids = (o.product_ids as string[]) ?? [];
    const split = ids.length > 0 ? Number(o.order_total) / ids.length : 0;
    for (const id of ids) {
      const t = tally.get(id) ?? { orders: 0, revenue: 0 };
      t.orders += 1;
      t.revenue += split;
      tally.set(id, t);
    }
  }
  const top_products = [...tally.entries()]
    .map(([product_id, v]) => ({ product_id, ...v }))
    .sort((a, b) => b.revenue - a.revenue)
    .slice(0, 5);

  const recommendations: string[] = [];
  if ((runs.count ?? 0) > 0) recommendations.push('Investigate failed automations this week.');
  if ((flags.count ?? 0) > 0) recommendations.push('Review compliance flags before next publish.');
  if (orderRows.length === 0) recommendations.push('No orders this week — review listing SEO and image quality.');

  const report: WeeklyReport = {
    week_start,
    week_end,
    revenue,
    orders: orderRows.length,
    top_products,
    customer_messages: msgs.count ?? 0,
    refunds_or_issues: 0, // wired up when refund flow exists
    failed_automations: runs.count ?? 0,
    compliance_flags: flags.count ?? 0,
    recommendations,
  };

  // Persist.
  await supa.from('weekly_reports').upsert(
    {
      week_start,
      week_end,
      revenue,
      orders: orderRows.length,
      top_products,
      issues: { failed_automations: runs.count ?? 0, compliance_flags: flags.count ?? 0 },
      recommendations,
    },
    { onConflict: 'week_start,week_end' },
  );

  return {
    output: report,
    confidence: 'high',
    assumptions: ['Revenue split evenly across products in multi-item orders.'],
    compliance_concerns: [],
    human_review_required: false,
    suggested_next_action: 'Read report; act on any flagged recommendations.',
  };
}
