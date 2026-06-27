import { syncOrders } from '../agents/orders.js';
import { logAutomationRun } from '../db/index.js';

/** Workflow 3 — Order Sync (cron-driven). */
export async function orderSyncWorkflow(): Promise<void> {
  const t0 = Date.now();
  const since = Math.floor((Date.now() - 24 * 60 * 60 * 1000) / 1000);
  try {
    const r = await syncOrders(since);
    await logAutomationRun({
      workflow_name: 'order_sync',
      trigger: 'cron',
      output_summary: JSON.stringify(r.output),
      success: true,
      duration_ms: Date.now() - t0,
    });
  } catch (err) {
    await logAutomationRun({
      workflow_name: 'order_sync',
      trigger: 'cron',
      success: false,
      error_message: String((err as Error).message),
      duration_ms: Date.now() - t0,
    });
    throw err;
  }
}
