import { createHash, randomBytes } from 'node:crypto';
import { assertEtsyConfigured, env, etsyRedirectUri, etsyScopes } from '../../config.js';
import { logger } from '../../lib/logger.js';

/**
 * Etsy Open API v3 OAuth 2.0 (Authorization Code + PKCE).
 * Reference: https://developer.etsy.com/documentation/essentials/authentication/
 */
const ETSY_OAUTH_AUTHORIZE = 'https://www.etsy.com/oauth/connect';
const ETSY_OAUTH_TOKEN = 'https://api.etsy.com/v3/public/oauth/token';

export interface PkcePair {
  code_verifier: string;
  code_challenge: string;
}

export function generatePkcePair(): PkcePair {
  const verifier = base64url(randomBytes(48));
  const challenge = base64url(createHash('sha256').update(verifier).digest());
  return { code_verifier: verifier, code_challenge: challenge };
}

export interface AuthorizeUrlInput {
  state: string;
  code_challenge: string;
  scopes?: string;
}

export function buildAuthorizeUrl(input: AuthorizeUrlInput): string {
  assertEtsyConfigured();
  if (!etsyRedirectUri) {
    throw new Error('ETSY_REDIRECT_URI is required');
  }
  const params = new URLSearchParams({
    response_type: 'code',
    client_id: env.ETSY_KEYSTRING!,
    redirect_uri: etsyRedirectUri,
    scope: (input.scopes ?? etsyScopes).split(/\s+/).join(' '),
    state: input.state,
    code_challenge: input.code_challenge,
    code_challenge_method: 'S256',
  });
  return `${ETSY_OAUTH_AUTHORIZE}?${params.toString()}`;
}

export interface OAuthTokens {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  token_type: string;
}

export async function exchangeAuthorizationCode(input: {
  code: string;
  code_verifier: string;
}): Promise<OAuthTokens> {
  assertEtsyConfigured();
  const body = new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: env.ETSY_KEYSTRING!,
    redirect_uri: etsyRedirectUri!,
    code: input.code,
    code_verifier: input.code_verifier,
  });
  const res = await fetch(ETSY_OAUTH_TOKEN, {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Etsy OAuth token exchange failed: ${res.status} ${text}`);
  }
  const tokens = (await res.json()) as OAuthTokens;
  logger.info({ expires_in: tokens.expires_in }, 'etsy.oauth.exchange.ok');
  return tokens;
}

export async function refreshTokens(refresh_token: string): Promise<OAuthTokens> {
  assertEtsyConfigured();
  const body = new URLSearchParams({
    grant_type: 'refresh_token',
    client_id: env.ETSY_KEYSTRING!,
    refresh_token,
  });
  const res = await fetch(ETSY_OAUTH_TOKEN, {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Etsy OAuth refresh failed: ${res.status} ${text}`);
  }
  const tokens = (await res.json()) as OAuthTokens;
  logger.info({ expires_in: tokens.expires_in }, 'etsy.oauth.refresh.ok');
  return tokens;
}

function base64url(buf: Buffer): string {
  return buf.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
