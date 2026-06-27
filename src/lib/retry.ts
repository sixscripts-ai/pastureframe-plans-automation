import { logger } from './logger.js';

export interface RetryOptions {
  maxAttempts?: number;
  baseDelayMs?: number;
  maxDelayMs?: number;
  /** Called for each attempt; throw to abort, return delay override, or void */
  onRetry?: (err: unknown, attempt: number) => number | void;
}

export async function retry<T>(
  fn: () => Promise<T>,
  opts: RetryOptions = {},
): Promise<T> {
  const max = opts.maxAttempts ?? 5;
  const base = opts.baseDelayMs ?? 500;
  const cap = opts.maxDelayMs ?? 30_000;

  let lastErr: unknown;
  for (let attempt = 1; attempt <= max; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      if (attempt === max) break;
      const override = opts.onRetry?.(err, attempt);
      const delay =
        typeof override === 'number'
          ? override
          : Math.min(cap, base * 2 ** (attempt - 1)) + Math.random() * 250;
      logger.warn({ err, attempt, delay }, 'retry.backoff');
      await new Promise((r) => setTimeout(r, delay));
    }
  }
  throw lastErr;
}
