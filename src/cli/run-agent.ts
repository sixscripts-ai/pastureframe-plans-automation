import { newProductWorkflow } from '../workflows/new_product.js';
import { messageIntakeWorkflow } from '../workflows/message_intake.js';
import { reviewCompliance } from '../agents/compliance.js';
import { draftListing } from '../agents/listing.js';

const which = process.argv[2];

switch (which) {
  case 'product': {
    // Demo run — replace with real product input.
    const r = await newProductWorkflow({
      product_name: 'Demo Product',
      product_type: 'mobile_coop',
      target_customer: 'Backyard homesteader with 0.25-2 acres.',
      specifications: ['10x10 base', '4x10 elevated coop'],
      features_for_listing: ['Mobile', 'Predator-resistant latches', 'Sloped roof', 'Ventilation'],
      price: 39,
    });
    console.log(JSON.stringify(r, null, 2));
    break;
  }
  case 'listing': {
    const r = await draftListing({
      product_name: 'Demo Listing',
      product_type: 'mobile_coop',
      target_customer: 'Backyard homesteaders.',
      features: ['Mobile', '10x10 run'],
      price: 39,
    });
    console.log(JSON.stringify(r, null, 2));
    break;
  }
  case 'compliance': {
    const text = process.argv[3] ?? '';
    const r = await reviewCompliance({ surface: 'listing', text });
    console.log(JSON.stringify(r, null, 2));
    break;
  }
  case 'customer-service': {
    const text = process.argv[3] ?? '';
    const buyer = process.argv[4] ?? 'demo-buyer';
    const r = await messageIntakeWorkflow({ buyer_user_id: buyer, raw_message: text });
    console.log(JSON.stringify(r, null, 2));
    break;
  }
  default:
    console.error('Usage: run-agent.ts product|listing|compliance|customer-service [args...]');
    process.exit(1);
}
