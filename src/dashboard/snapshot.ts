import { db } from '../db/index.js';

/**
 * Dashboard query layer. The actual UI (Phase 2) renders these as cards.
 */
export interface DashboardSnapshot {
  active_products: number;
  draft_products: number;
  listings_pending_approval: number;
  orders_this_week: number;
  revenue_this_week: number;
  top_products: Array<{ product_id: string; orders: number }>;
  pending_messages: number;
  customer_issues: number;
  failed_automations_24h: number;
  compliance_flags_high: number;
  recommended_actions: string[];
}

export async function snapshot(): Promise<DashboardSnapshot> {
  const supa = db();
  const weekStart = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();
  const dayStart = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();

  const [active, drafts, pending, orders, msgs, runs, flags] = await Promise.all([
    supa.from('products').select('product_id', { count: 'exact', head: true }).eq('status', 'listed'),
    supa.from('products').select('product_id', { count: 'exact', head: true }).eq('status', 'draft'),
    supa
      .from('listing_metadata')
      .select('listing_id', { count: 'exact', head: true })
      .eq('approval_status', 'pending'),
    supa
      .from('orders')
      .select('order_total, product_ids')
      .gte('purchase_date', weekStart),
    supa
      .from('customer_messages')
      .select('message_id', { count: 'exact', head: true })
      .eq('approval_status', 'pending'),
    supa
      .from('automation_runs')
      .select('run_id', { count: 'exact', head: true })
      .eq('success', false)
      .gte('timestamp', dayStart),
    supa
      .from('compliance_log')
      .select('log_id', { count: 'exact', head: true })
      .eq('severity', 'high'),
  ]);

  const orderRows = orders.data ?? [];
  const revenue = orderRows.reduce((s, o) => s + Number(o.order_total ?? 0), 0);
  const tally = new Map<string, number>();
  for (const o of orderRows) for (const p of (o.product_ids as string[]) ?? []) tally.set(p, (tally.get(p) ?? 0) + 1);
  const top_products = [...tally.entries()].map(([product_id, n]) => ({ product_id, orders: n })).sort((a, b) => b.orders - a.orders).slice(0, 5);

  const recs: string[] = [];
  if ((pending.count ?? 0) > 0) recs.push(`${pending.count} listings waiting on approval.`);
  if ((msgs.count ?? 0) > 0) recs.push(`${msgs.count} customer messages waiting on approval.`);
  if ((runs.count ?? 0) > 0) recs.push(`${runs.count} automations failed in last 24h.`);
  if ((flags.count ?? 0) > 0) recs.push(`${flags.count} high-severity compliance flags open.`);
  if (orderRows.length === 0) recs.push('No orders this week.');

  return {
    active_products: active.count ?? 0,
    draft_products: drafts.count ?? 0,
    listings_pending_approval: pending.count ?? 0,
    orders_this_week: orderRows.length,
    revenue_this_week: revenue,
    top_products,
    pending_messages: msgs.count ?? 0,
    customer_issues: 0,
    failed_automations_24h: runs.count ?? 0,
    compliance_flags_high: flags.count ?? 0,
    recommended_actions: recs,
  };
}
