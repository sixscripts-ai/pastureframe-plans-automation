import { createDraftListing, setListingTypeDownload } from '../api/etsy/listings.js';
import { db, logAutomationRun, logCompliance } from '../db/index.js';
import { reviewCompliance } from '../agents/compliance.js';
import { assertNotEmergencyStopped } from '../config.js';
import { logger } from '../lib/logger.js';

/**
 * Workflow 2 — Listing Draft Creation (HUMAN-APPROVED ONLY).
 * Reads listing_metadata where approval_status='approved' AND last_published_at IS NULL.
 * Calls Etsy API to create a draft listing, sets type=download, stores listing_id.
 * Does NOT publish (Etsy publishes only when state moves to "active" — that
 * remains a manual operator step or a separately gated workflow).
 */
export async function publishApprovedDrafts(): Promise<{ created: number; skipped: number }> {
  assertNotEmergencyStopped();
  const t0 = Date.now();
  let created = 0;
  let skipped = 0;
  try {
    const supa = db();
    const { data, error } = await supa
      .from('listing_metadata')
      .select('*')
      .eq('approval_status', 'approved')
      .is('last_published_at', null)
      .limit(10);
    if (error) throw error;

    for (const l of data ?? []) {
      // Re-run compliance immediately before any side-effect.
      const c = await reviewCompliance({
        surface: 'listing',
        text: l.description,
        has_digital_only_disclosure: /digital download/i.test(l.description),
        has_personal_use_license: /personal use/i.test(l.description),
        has_diy_disclaimer: /local code|verify/i.test(l.description),
      });
      if (!c.output.pass) {
        await logCompliance({
          event_type: 'block',
          system_area: 'listing',
          issue: 'Last-mile compliance failed at publish.',
          severity: 'high',
          related_id: l.listing_id,
          action_taken: 'publish_blocked',
        });
        skipped++;
        continue;
      }

      const draft = await createDraftListing({
        title: l.title,
        description: l.description,
        price: l.price,
        quantity: l.quantity,
        taxonomy_id: l.taxonomy_id,
        who_made: 'i_did',
        when_made: 'made_to_order',
        type: 'download',
        tags: l.tags,
      });
      await setListingTypeDownload(draft.listing_id);

      await supa
        .from('listing_metadata')
        .update({ last_published_at: new Date().toISOString() })
        .eq('listing_id', l.listing_id);
      await supa
        .from('products')
        .update({ etsy_listing_id: draft.listing_id, etsy_listing_status: draft.state })
        .eq('product_id', l.product_id);
      created++;
    }

    await logAutomationRun({
      workflow_name: 'listing_draft_creation',
      trigger: 'cron',
      output_summary: `created=${created} skipped=${skipped}`,
      success: true,
      duration_ms: Date.now() - t0,
    });
    return { created, skipped };
  } catch (err) {
    logger.error({ err }, 'workflow.publish_listing.fail');
    await logAutomationRun({
      workflow_name: 'listing_draft_creation',
      trigger: 'cron',
      success: false,
      error_message: String((err as Error).message),
      duration_ms: Date.now() - t0,
    });
    throw err;
  }
}
