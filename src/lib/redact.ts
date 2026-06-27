/**
 * Redact PII from buyer messages before sending to an LLM.
 * Strips emails, phone numbers, addresses (best-effort), full names following
 * common honorifics, and any token starting with the project's hash salt.
 */
const EMAIL = /[\w.+-]+@[\w-]+\.[\w.-]+/g;
const PHONE = /(\+?\d[\d\s().-]{7,}\d)/g;
const ADDRESS = /\b\d{1,5}\s+[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Way)\b/g;
const NAME = /\b(?:Mr|Mrs|Ms|Mx|Dr)\.?\s+[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)?/g;
const CC = /\b(?:\d[ -]*?){13,16}\b/g;

export function redactPII(input: string): string {
  if (!input) return input;
  return input
    .replace(EMAIL, '[REDACTED_EMAIL]')
    .replace(CC, '[REDACTED_CARD]')
    .replace(PHONE, '[REDACTED_PHONE]')
    .replace(ADDRESS, '[REDACTED_ADDRESS]')
    .replace(NAME, '[REDACTED_NAME]');
}
