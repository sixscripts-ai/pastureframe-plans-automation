import { env, assertEtsyConfigured, assertNotEmergencyStopped } from '../../config.js';
import { logger } from '../../lib/logger.js';
import { retry } from '../../lib/retry.js';
import { refreshTokens } from './oauth.js';

const ETSY_BASE = 'https://api.etsy.com/v3/application';

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body?: unknown;
  query?: Record<string, string | number | boolean | undefined>;
  /** When true, performs a write — gets blocked by EMERGENCY_STOP. */
  mutating?: boolean;
}

/**
 * Mutable in-memory token store; in production back this with the database.
 */
const tokens = {
  access_token: env.ETSY_ACCESS_TOKEN,
  refresh_token: env.ETSY_REFRESH_TOKEN,
  expires_at: env.ETSY_TOKEN_EXPIRES_AT
    ? Number(env.ETSY_TOKEN_EXPIRES_AT)
    : 0,
};

async function ensureAccessToken(): Promise<string> {
  if (!tokens.refresh_token) {
    throw new Error('Etsy not authorized: run `npm run etsy:auth` first');
  }
  const now = Math.floor(Date.now() / 1000);
  if (!tokens.access_token || tokens.expires_at - 60 < now) {
    const fresh = await refreshTokens(tokens.refresh_token);
    tokens.access_token = fresh.access_token;
    tokens.refresh_token = fresh.refresh_token;
    tokens.expires_at = now + fresh.expires_in;
  }
  return tokens.access_token!;
}

export async function etsyRequest<T = unknown>(
  path: string,
  opts: RequestOptions = {},
): Promise<T> {
  if (opts.mutating) assertNotEmergencyStopped();
  assertEtsyConfigured();

  const accessToken = await ensureAccessToken();
  const url = new URL(ETSY_BASE + path);
  for (const [k, v] of Object.entries(opts.query ?? {})) {
    if (v !== undefined) url.searchParams.set(k, String(v));
  }

  return retry(
    async () => {
      const res = await fetch(url.toString(), {
        method: opts.method ?? 'GET',
        headers: {
          // Etsy expects keystring + shared secret colon-separated.
          'x-api-key': `${env.ETSY_KEYSTRING}:${env.ETSY_SHARED_SECRET}`,
          authorization: `Bearer ${accessToken}`,
          'content-type': 'application/json',
          accept: 'application/json',
        },
        body: opts.body ? JSON.stringify(opts.body) : undefined,
      });

      if (res.status === 429 || res.status >= 500) {
        const retryAfter = Number(res.headers.get('retry-after')) || 0;
        const err = new Error(`Etsy ${res.status}`);
        (err as Error & { retryAfter?: number }).retryAfter = retryAfter * 1000;
        throw err;
      }
      if (!res.ok) {
        const text = await res.text();
        // 4xx — don't retry; surface to operator.
        const err = new Error(`Etsy ${res.status}: ${text}`);
        (err as Error & { noRetry?: boolean }).noRetry = true;
        throw err;
      }
      return (await res.json()) as T;
    },
    {
      maxAttempts: 5,
      onRetry: (err) => {
        const e = err as Error & { retryAfter?: number; noRetry?: boolean };
        if (e.noRetry) throw err;
        return e.retryAfter;
      },
    },
  );
}

/** Daily heartbeat to avoid 6-month dormancy ban. */
export async function heartbeat(): Promise<void> {
  if (!env.ETSY_SHOP_ID) return;
  await etsyRequest(`/shops/${env.ETSY_SHOP_ID}`);
  logger.info('etsy.heartbeat.ok');
}
