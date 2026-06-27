import { draftProductPackage } from '../agents/product_dev.js';
import { draftListing } from '../agents/listing.js';
import { reviewCompliance } from '../agents/compliance.js';
import { logAutomationRun } from '../db/index.js';
import { logger } from '../lib/logger.js';

/**
 * Workflow 1 — New Product Creation.
 * Drafts the product package, then a listing draft, then runs compliance.
 * Output is queued for human review; nothing is published.
 */
export interface NewProductInput {
  product_name: string;
  product_type: string;
  target_customer: string;
  specifications: string[];
  optional_features?: string[];
  features_for_listing: string[];
  price: number;
}

export async function newProductWorkflow(input: NewProductInput): Promise<{
  ok: boolean;
  pkg: unknown;
  listing: unknown;
  compliance: unknown;
}> {
  const t0 = Date.now();
  try {
    const pkg = await draftProductPackage({
      product_name: input.product_name,
      product_type: input.product_type,
      specifications: input.specifications,
      optional_features: input.optional_features,
    });
    const listing = await draftListing({
      product_name: input.product_name,
      product_type: input.product_type,
      target_customer: input.target_customer,
      features: input.features_for_listing,
      price: input.price,
    });
    const compliance = await reviewCompliance({
      surface: 'listing',
      text: listing.output.description ?? '',
      has_digital_only_disclosure: /digital download/i.test(listing.output.description ?? ''),
      has_personal_use_license: /personal use/i.test(listing.output.description ?? ''),
      has_diy_disclaimer: /local code|verify/i.test(listing.output.description ?? ''),
    });

    await logAutomationRun({
      workflow_name: 'new_product_creation',
      trigger: 'manual',
      input_summary: input.product_name,
      output_summary: `pkg:${pkg.confidence} listing:${listing.confidence} compliance:${compliance.output.pass}`,
      success: true,
      duration_ms: Date.now() - t0,
    });
    return { ok: compliance.output.pass, pkg, listing, compliance };
  } catch (err) {
    logger.error({ err }, 'workflow.new_product.fail');
    await logAutomationRun({
      workflow_name: 'new_product_creation',
      trigger: 'manual',
      input_summary: input.product_name,
      success: false,
      error_message: String((err as Error).message),
      duration_ms: Date.now() - t0,
    });
    throw err;
  }
}
