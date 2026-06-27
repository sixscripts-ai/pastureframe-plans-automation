import { listReceipts } from '../api/etsy/listings.js';
import { db } from '../db/index.js';
import { hashBuyerId } from '../lib/hash.js';
import { logger } from '../lib/logger.js';
import type { AgentEnvelope } from './types.js';

/** Agent 5 — Order Operations Agent. Read-only sync of Etsy receipts. */
export interface OrderSyncResult {
  synced: number;
  duplicates_skipped: number;
  issues_flagged: number;
}

interface EtsyReceiptListResponse {
  count: number;
  results: EtsyReceipt[];
}

interface EtsyReceipt {
  receipt_id: number;
  buyer_user_id: number | string;
  name?: string;
  created_timestamp: number;
  status: string;
  grandtotal?: { amount: number; divisor: number; currency_code?: string };
  is_paid?: boolean;
  is_shipped?: boolean;
  transactions?: Array<{ listing_id: number; product_id?: number }>;
}

export async function syncOrders(sinceUnixSec?: number): Promise<AgentEnvelope<OrderSyncResult>> {
  const result: OrderSyncResult = { synced: 0, duplicates_skipped: 0, issues_flagged: 0 };
  const issues: string[] = [];

  try {
    const data = (await listReceipts({ min_created: sinceUnixSec })) as EtsyReceiptListResponse;
    const receipts = data?.results ?? [];

    for (const r of receipts) {
      const total = r.grandtotal ? r.grandtotal.amount / r.grandtotal.divisor : 0;
      const buyer_id_hash = hashBuyerId(r.buyer_user_id);
      const row = {
        etsy_receipt_id: r.receipt_id,
        buyer_id_hash,
        purchase_date: new Date(r.created_timestamp * 1000).toISOString(),
        product_ids: [], // resolved separately by mapping listing_id -> product_id
        order_total: total,
        order_status: r.status,
        fulfillment_status: 'digital_auto' as const,
      };

      const { error } = await db()
        .from('orders')
        .upsert(row, { onConflict: 'etsy_receipt_id', ignoreDuplicates: true });
      if (error) {
        issues.push(`receipt ${r.receipt_id}: ${error.message}`);
        result.issues_flagged++;
      } else {
        result.synced++;
      }
    }
    logger.info({ ...result }, 'orders.sync.ok');
  } catch (err) {
    logger.error({ err }, 'orders.sync.fail');
    issues.push(String((err as Error).message));
    result.issues_flagged++;
  }

  return {
    output: result,
    confidence: 'high',
    assumptions: ['Receipts endpoint paginated externally; first 100 only here.'],
    compliance_concerns: [],
    human_review_required: result.issues_flagged > 0,
    suggested_next_action: issues.length ? `Investigate: ${issues.join('; ')}` : 'No action needed.',
  };
}
