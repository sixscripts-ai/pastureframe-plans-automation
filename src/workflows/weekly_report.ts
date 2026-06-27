import { generateWeeklyReport } from '../agents/analytics.js';
import { logAutomationRun } from '../db/index.js';

/** Workflow 5 — Weekly Report. */
export async function weeklyReportWorkflow() {
  const t0 = Date.now();
  try {
    const report = await generateWeeklyReport();
    await logAutomationRun({
      workflow_name: 'weekly_report',
      trigger: 'cron',
      output_summary: `revenue=${report.output.revenue} orders=${report.output.orders}`,
      success: true,
      duration_ms: Date.now() - t0,
    });
    return report;
  } catch (err) {
    await logAutomationRun({
      workflow_name: 'weekly_report',
      trigger: 'cron',
      success: false,
      error_message: String((err as Error).message),
      duration_ms: Date.now() - t0,
    });
    throw err;
  }
}
