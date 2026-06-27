import pino from 'pino';
import { env } from '../config.js';

export const logger = pino({
  level: env.LOG_LEVEL,
  redact: {
    paths: [
      'access_token',
      'refresh_token',
      '*.access_token',
      '*.refresh_token',
      'authorization',
      '*.authorization',
      'x-api-key',
      '*.x-api-key',
      'buyer_email',
      '*.buyer_email',
    ],
    censor: '[REDACTED]',
  },
});
