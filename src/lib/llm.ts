import Anthropic from '@anthropic-ai/sdk';
import OpenAI from 'openai';
import { env } from '../config.js';

export interface LlmRequest {
  system: string;
  user: string;
  /** json | text */
  responseFormat?: 'json' | 'text';
  maxTokens?: number;
}

export interface LlmResponse<T = unknown> {
  text: string;
  json?: T;
  provider: 'anthropic' | 'openai';
  model: string;
}

let _anthropic: Anthropic | null = null;
let _openai: OpenAI | null = null;

export async function callLLM<T = unknown>(req: LlmRequest): Promise<LlmResponse<T>> {
  try {
    return await callAnthropic<T>(req);
  } catch (err) {
    if (env.OPENAI_API_KEY) return await callOpenAI<T>(req);
    throw err;
  }
}

async function callAnthropic<T>(req: LlmRequest): Promise<LlmResponse<T>> {
  if (!env.ANTHROPIC_API_KEY) throw new Error('ANTHROPIC_API_KEY not set');
  _anthropic ??= new Anthropic({ apiKey: env.ANTHROPIC_API_KEY });
  const resp = await _anthropic.messages.create({
    model: env.LLM_MODEL,
    max_tokens: req.maxTokens ?? 2048,
    system: req.system,
    messages: [{ role: 'user', content: req.user }],
  });
  const text = resp.content
    .map((c) => (c.type === 'text' ? c.text : ''))
    .join('')
    .trim();
  return wrap<T>(text, 'anthropic', env.LLM_MODEL, req.responseFormat);
}

async function callOpenAI<T>(req: LlmRequest): Promise<LlmResponse<T>> {
  if (!env.OPENAI_API_KEY) throw new Error('OPENAI_API_KEY not set');
  _openai ??= new OpenAI({ apiKey: env.OPENAI_API_KEY });
  const model = 'gpt-4o-mini';
  const resp = await _openai.chat.completions.create({
    model,
    max_tokens: req.maxTokens ?? 2048,
    messages: [
      { role: 'system', content: req.system },
      { role: 'user', content: req.user },
    ],
    response_format: req.responseFormat === 'json' ? { type: 'json_object' } : undefined,
  });
  const text = resp.choices[0]?.message?.content?.trim() ?? '';
  return wrap<T>(text, 'openai', model, req.responseFormat);
}

function wrap<T>(
  text: string,
  provider: 'anthropic' | 'openai',
  model: string,
  fmt?: 'json' | 'text',
): LlmResponse<T> {
  let json: T | undefined;
  if (fmt === 'json') {
    try {
      json = JSON.parse(text) as T;
    } catch {
      const m = text.match(/\{[\s\S]*\}/);
      if (m) {
        try {
          json = JSON.parse(m[0]) as T;
        } catch {
          /* ignore */
        }
      }
    }
  }
  return { text, json, provider, model };
}
