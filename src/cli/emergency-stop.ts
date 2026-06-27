/**
 * Sets EMERGENCY_STOP=true for the running process. To halt scheduled jobs,
 * set the env var in your platform (Cloudflare Workers vars, Supabase
 * Functions secrets, n8n env). This script writes a sentinel file so a
 * companion check can refuse side effects even without the env var.
 */
import { writeFileSync } from 'node:fs';
const path = '.emergency_stop';
writeFileSync(path, new Date().toISOString());
console.log('Emergency stop sentinel written:', path);
console.log('Also set EMERGENCY_STOP=true in your platform env to halt all writes.');
