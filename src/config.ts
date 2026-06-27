import 'dotenv/config';
import { z } from 'zod';

const Env = z.object({
  // App
  APP_NAME: z.string().default('PastureFrame Plans Automation'),
  APP_ENV: z.enum(['development', 'production', 'test']).default('development'),
  APP_BASE_URL: z.string().url().default('http://localhost:3000'),

  // Etsy
  ETSY_API_BASE_URL: z.string().url().default('https://api.etsy.com/v3/application'),
  ETSY_KEYSTRING: z.string().min(1).optional(),
  ETSY_SHARED_SECRET: z.string().min(1).optional(),
  ETSY_CLIENT_ID: z.string().optional(),
  ETSY_USER_ID: z.string().optional(),
  ETSY_SHOP_ID: z.string().optional(),
  ETSY_REDIRECT_URI: z.string().url().optional(),
  ETSY_SCOPES: z.string().default('listings_r listings_w shops_r shops_w transactions_r'),
  ETSY_OAUTH_REDIRECT_URI: z.string().url().optional(),
  ETSY_OAUTH_SCOPES: z.string().optional(),
  ETSY_ACCESS_TOKEN: z.string().optional(),
  ETSY_REFRESH_TOKEN: z.string().optional(),
  ETSY_TOKEN_EXPIRES_AT: z.string().optional(),
  ETSY_OAUTH_STATE_SECRET: z.string().optional(),
  ETSY_CODE_VERIFIER_SECRET: z.string().optional(),

  // Automation Safety
  AUTOMATION_ENABLED: z
    .string()
    .default('false')
    .transform((v) => v === 'true'),
  REQUIRE_HUMAN_APPROVAL: z
    .string()
    .default('true')
    .transform((v) => v !== 'false'),
  ALLOW_AUTO_PUBLISH: z
    .string()
    .default('false')
    .transform((v) => v === 'true'),
  ALLOW_AUTO_PRICE_CHANGES: z
    .string()
    .default('false')
    .transform((v) => v === 'true'),
  ALLOW_AUTO_CUSTOMER_MESSAGES: z
    .string()
    .default('false')
    .transform((v) => v === 'true'),

  // DB
  SUPABASE_URL: z.string().url().optional(),
  SUPABASE_SERVICE_ROLE_KEY: z.string().optional(),

  // LLM
  ANTHROPIC_API_KEY: z.string().optional(),
  OPENAI_API_KEY: z.string().optional(),
  LLM_PROVIDER: z.enum(['anthropic', 'openai']).default('anthropic'),
  LLM_MODEL: z.string().default('claude-3-5-sonnet-latest'),

  // Security
  BUYER_ID_HASH_SALT: z.string().min(8).default('dev-only-salt-change-me'),
  EMERGENCY_STOP: z
    .string()
    .default('false')
    .transform((v) => v === 'true'),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),

  // Server
  PORT: z.coerce.number().default(3000),
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
});

export type EnvConfig = z.infer<typeof Env>;
export const env: EnvConfig = Env.parse(process.env);

export const etsyRedirectUri = env.ETSY_REDIRECT_URI ?? env.ETSY_OAUTH_REDIRECT_URI;
export const etsyScopes = env.ETSY_SCOPES ?? env.ETSY_OAUTH_SCOPES ?? 'listings_r listings_w shops_r shops_w transactions_r';

export function assertEtsyConfigured(): void {
  if (!env.ETSY_KEYSTRING || !env.ETSY_SHARED_SECRET) {
    throw new Error('Etsy API not configured: set ETSY_KEYSTRING and ETSY_SHARED_SECRET');
  }
}

export function assertNotEmergencyStopped(): void {
  if (env.EMERGENCY_STOP) {
    throw new Error('EMERGENCY_STOP is active. All side-effecting operations are halted.');
  }
}
