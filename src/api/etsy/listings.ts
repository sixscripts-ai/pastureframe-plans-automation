import { env } from '../../config.js';
import { etsyRequest } from './client.js';

/**
 * Listings endpoints — wrappers around the Etsy Open API v3.
 * Reference: https://developer.etsy.com/documentation/tutorials/listings/
 *
 * NOTE: Every mutating call passes `mutating: true` so that EMERGENCY_STOP
 * blocks the request. Publish/edit operations must additionally be gated by
 * a human-approved row in `listing_metadata`.
 */

export interface DraftListingInput {
  title: string;
  description: string;
  price: number;
  quantity?: number;
  taxonomy_id: number;
  who_made: 'i_did' | 'someone_else' | 'collective';
  when_made: 'made_to_order' | string;
  type?: 'physical' | 'download' | 'both';
  tags?: string[];
}

export interface DraftListingResponse {
  listing_id: number;
  state: string;
  url?: string;
}

export async function createDraftListing(
  input: DraftListingInput,
): Promise<DraftListingResponse> {
  if (!env.ETSY_SHOP_ID) throw new Error('ETSY_SHOP_ID not configured');
  if ((input.tags?.length ?? 0) > 13) throw new Error('Etsy allows max 13 tags');
  if (input.title.length > 140) throw new Error('Etsy title max 140 chars');

  const body = {
    quantity: input.quantity ?? 999,
    title: input.title,
    description: input.description,
    price: input.price,
    who_made: input.who_made,
    when_made: input.when_made,
    taxonomy_id: input.taxonomy_id,
    tags: input.tags ?? [],
    type: input.type ?? 'download',
  };
  return etsyRequest<DraftListingResponse>(
    `/shops/${env.ETSY_SHOP_ID}/listings`,
    { method: 'POST', body, mutating: true },
  );
}

export async function setListingTypeDownload(listing_id: number): Promise<void> {
  if (!env.ETSY_SHOP_ID) throw new Error('ETSY_SHOP_ID not configured');
  await etsyRequest(
    `/shops/${env.ETSY_SHOP_ID}/listings/${listing_id}`,
    { method: 'PATCH', body: { type: 'download' }, mutating: true },
  );
}

export async function getShop(): Promise<unknown> {
  if (!env.ETSY_SHOP_ID) throw new Error('ETSY_SHOP_ID not configured');
  return etsyRequest(`/shops/${env.ETSY_SHOP_ID}`);
}

export interface ReceiptListInput {
  min_created?: number; // unix seconds
  limit?: number;
  offset?: number;
}

export async function listReceipts(input: ReceiptListInput = {}): Promise<unknown> {
  if (!env.ETSY_SHOP_ID) throw new Error('ETSY_SHOP_ID not configured');
  return etsyRequest(`/shops/${env.ETSY_SHOP_ID}/receipts`, {
    query: {
      min_created: input.min_created,
      limit: input.limit ?? 100,
      offset: input.offset ?? 0,
    },
  });
}
