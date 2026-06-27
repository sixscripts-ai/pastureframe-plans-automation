import { createServer } from 'node:http';
import { env } from './config.js';
import { logger } from './lib/logger.js';

/**
 * Tiny health/status server. Cloudflare Worker (or any host) front-end.
 * The OAuth callback endpoint is sketched but not wired to a frontend.
 */
const server = createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ ok: true, env: env.NODE_ENV, emergency_stop: env.EMERGENCY_STOP }));
    return;
  }
  if (req.url?.startsWith('/oauth/etsy/callback')) {
    res.writeHead(200, { 'content-type': 'text/plain' });
    res.end(
      'OAuth callback received. Copy the `code` query param and run `tsx src/cli/etsy-oauth.ts exchange <code> <verifier>`.',
    );
    return;
  }
  res.writeHead(404);
  res.end('not found');
});

server.listen(env.PORT, () => {
  logger.info({ port: env.PORT }, 'server.up');
});
