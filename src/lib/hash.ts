import { createHash } from 'node:crypto';
import { env } from '../config.js';

/** Hash a buyer identifier with a salt before persistence. */
export function hashBuyerId(buyerUserId: string | number): string {
  return createHash('sha256')
    .update(`${buyerUserId}:${env.BUYER_ID_HASH_SALT}`)
    .digest('hex');
}
