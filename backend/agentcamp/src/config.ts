import { z } from 'zod';

const origin = z.string().url().refine((s) => new URL(s).origin === s, 'Use an origin without a trailing slash or path');
const envSchema = z.object({
  AGENTCAMP_APP_ID: z.string().regex(/^cli_[a-zA-Z0-9]+$/),
  AGENTCAMP_APP_SECRET: z.string().min(1),
  AGENTCAMP_BASE_TOKEN: z.string().regex(/^[a-zA-Z0-9]+$/),
  AGENTCAMP_TABLE_ID: z.string().regex(/^tbl[a-zA-Z0-9]+$/),
  AGENTCAMP_CHAT_ID: z.string().regex(/^oc_[a-zA-Z0-9]+$/),
  AGENTCAMP_BASE_URL: z.string().url().refine((s) => {
    const u = new URL(s);
    return u.protocol === 'https:' && u.hostname.endsWith('.feishu.cn') && /^\/(base|wiki)\/[a-zA-Z0-9]+$/.test(u.pathname) && !u.search && !u.hash && !u.username && !u.password;
  }, 'Use the confirmed SDR Base URL without query or fragment'),
  AGENTCAMP_ORIGINS: z.string().transform((s) => s.split(',').map((v) => v.trim())).pipe(z.array(origin).min(1)),
  AGENTCAMP_DB_PATH: z.string().min(1),
  AGENTCAMP_PORT: z.coerce.number().int().min(1).max(65535).default(3010),
  AGENTCAMP_TRUST_PROXY: z.enum(['true', 'false']).default('false'),
  AGENTCAMP_ENV: z.enum(['production', 'preview']).default('production')
});

export type Config = z.infer<typeof envSchema>;

export function readConfig(env: NodeJS.ProcessEnv = process.env): Config {
  const result = envSchema.safeParse(env);
  if (!result.success) {
    // Never print environment values, which include application credentials.
    throw new Error('Invalid configuration: ' + result.error.issues.map((i) => i.path.join('.')).join(', '));
  }
  return result.data;
}

const text = (max: number) => z.string().trim().max(max).refine((s) => !/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/.test(s));
export const applicationSchema = z.object({
  name: text(80).pipe(z.string().min(1)),
  company: text(200).pipe(z.string().min(1)),
  title: text(100).default(''),
  contact: text(254).refine((s) => z.email().safeParse(s).success || /^\+?[\d ()-]{7,25}$/.test(s) && s.replace(/\D/g, '').length >= 7),
  city: text(100).default(''),
  when: z.enum(['', '尽快', '一个月内', '一到三个月', '还没定']).default(''),
  task: text(3000).pipe(z.string().min(1)),
  data: z.enum(['', '能给静态样本', '要走审批', '还不确定']).default(''),
  agree: z.literal(true),
  page: z.literal('agentcamp')
}).strict();

export type Application = z.infer<typeof applicationSchema>;
