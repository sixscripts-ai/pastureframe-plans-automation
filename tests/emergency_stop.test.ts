import { describe, it, expect, beforeEach } from 'vitest';

describe('emergency stop', () => {
  beforeEach(() => {
    process.env.EMERGENCY_STOP = 'true';
  });

  it('blocks Etsy mutating requests when EMERGENCY_STOP=true', async () => {
    // Re-import config + client with the new env.
    delete (await import('../src/config.js')).default;
    process.env.ETSY_KEYSTRING = 'k';
    process.env.ETSY_SHARED_SECRET = 's';
    process.env.ETSY_REFRESH_TOKEN = 'rt';
    process.env.ETSY_TOKEN_EXPIRES_AT = String(Math.floor(Date.now() / 1000) + 3600);

    // Lazy import to pick up env.
    const { etsyRequest } = await import('../src/api/etsy/client.js');
    await expect(etsyRequest('/x', { method: 'POST', mutating: true })).rejects.toThrow(
      /EMERGENCY_STOP/,
    );
  });
});
