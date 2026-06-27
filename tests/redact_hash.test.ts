import { describe, it, expect } from 'vitest';
import { redactPII } from '../src/lib/redact.js';
import { hashBuyerId } from '../src/lib/hash.js';

describe('redactPII', () => {
  it('redacts emails and phone numbers', () => {
    const out = redactPII('Hi I am jane@example.com or (555) 123-4567');
    expect(out).not.toContain('jane@example.com');
    expect(out).not.toContain('555');
  });
  it('redacts credit cards', () => {
    const out = redactPII('card 4111 1111 1111 1111');
    expect(out).toContain('[REDACTED_CARD]');
  });
  it('redacts addresses', () => {
    const out = redactPII('I live at 123 Main Street near here.');
    expect(out).toContain('[REDACTED_ADDRESS]');
  });
});

describe('hashBuyerId', () => {
  it('returns deterministic 64-char hex', () => {
    const a = hashBuyerId(123456);
    const b = hashBuyerId('123456');
    expect(a).toMatch(/^[a-f0-9]{64}$/);
    expect(a).toBe(b);
  });
});
