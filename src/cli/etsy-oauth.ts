import { randomBytes } from 'node:crypto';
import { buildAuthorizeUrl, exchangeAuthorizationCode, generatePkcePair } from '../api/etsy/oauth.js';

/**
 * Two-step CLI:
 *   1) `npm run etsy:auth` — prints the authorize URL + state + verifier.
 *   2) Paste the `code` from the redirect into:
 *      `tsx src/cli/etsy-oauth.ts exchange <code> <verifier>`
 */
const args = process.argv.slice(2);

if (args[0] === 'exchange') {
  const code = args[1];
  const verifier = args[2];
  if (!code || !verifier) {
    console.error('Usage: tsx src/cli/etsy-oauth.ts exchange <code> <code_verifier>');
    process.exit(1);
  }
  const tokens = await exchangeAuthorizationCode({ code, code_verifier: verifier });
  console.log('Save these in your secret store (NEVER commit):');
  console.log(JSON.stringify(tokens, null, 2));
} else {
  const state = randomBytes(16).toString('hex');
  const pkce = generatePkcePair();
  const url = buildAuthorizeUrl({ state, code_challenge: pkce.code_challenge });
  console.log('1) Open this URL and approve:\n', url);
  console.log('\n2) After redirect, capture `code` from the URL and run:\n');
  console.log(`   tsx src/cli/etsy-oauth.ts exchange <code> ${pkce.code_verifier}\n`);
  console.log('state:', state);
}
