import 'reflect-metadata';
import { Controller, Get, Post, Req, Res, Inject, Module } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { NestExpressApplication } from '@nestjs/platform-express';
import { json, Request, Response } from 'express';
import { rateLimit } from 'express-rate-limit';
import helmet from 'helmet';
import { z } from 'zod';
import { Config, readConfig, applicationSchema } from './config';
import { Store, SubmissionConflict } from './store';
import { Feishu, Gateway } from './feishu';
import { Service } from './service';

@Controller('api/agentcamp')
class ApplicationsController {
  constructor(@Inject(Service) private service: Service) {}

  @Get('health')
  health() { return { ok: true }; }

  @Post('applications')
  async submit(@Req() req: Request, @Res() res: Response) {
    const payload = applicationSchema.safeParse(req.body);
    const id = z.uuid({ version: 'v4' }).safeParse(req.get('Idempotency-Key'));
    if (!payload.success || !id.success) return res.status(400).json({ ok: false, code: 'INVALID_INPUT' });
    try {
      const row = this.service.store.accept(id.data, payload.data);
      const result = await this.service.deliver(row.id);
      if (!result.record_id) return res.status(503).set('Retry-After', '10').json({ ok: false, code: 'PENDING', submissionId: row.id });
      return res.status(200).json({ ok: true, submissionId: row.id });
    } catch (error) {
      if (error instanceof SubmissionConflict) return res.status(409).json({ ok: false, code: 'IDEMPOTENCY_CONFLICT' });
      console.error('{"event":"agentcamp_submit_error"}');
      return res.status(503).json({ ok: false, code: 'UNAVAILABLE' });
    }
  }
}

export async function createApp(config: Config, options: { gateway?: Gateway; worker?: boolean; rateLimit?: number } = {}) {
  const store = new Store(config.AGENTCAMP_DB_PATH);
  const service = new Service(store, options.gateway || new Feishu(config));
  @Module({ controllers: [ApplicationsController], providers: [{ provide: Service, useValue: service }] })
  class AppModule {}
  const app = await NestFactory.create<NestExpressApplication>(AppModule, { logger: false, bodyParser: false });
  if (config.AGENTCAMP_TRUST_PROXY === 'true') app.set('trust proxy', 'loopback');
  app.use(helmet());
  app.use('/api/agentcamp', (_req: Request, res: Response, next: () => void) => { res.set('Cache-Control', 'no-store'); next(); });
  app.use('/api/agentcamp/applications', rateLimit({
    windowMs: 60000, limit: options.rateLimit ?? 10, standardHeaders: 'draft-8', legacyHeaders: false,
    message: { ok: false, code: 'RATE_LIMITED' }
  }));
  app.use('/api/agentcamp/applications', (req: Request, res: Response, next: () => void) => {
    if (req.method !== 'POST') { next(); return; }
    if (!config.AGENTCAMP_ORIGINS.includes(req.get('Origin') || '')) {
      res.status(403).json({ ok: false, code: 'ORIGIN_DENIED' }); return;
    }
    if (!req.is('application/json')) { res.status(415).json({ ok: false, code: 'JSON_REQUIRED' }); return; }
    next();
  });
  app.use(json({ limit: '16kb' }));
  await app.init();
  if (options.worker !== false) service.start();
  return { app, store, service, close: async () => { await app.close(); await service.stop(); store.close(); } };
}

async function main() {
  const config = readConfig();
  const gateway = new Feishu(config);
  await gateway.verifyDestination();
  if (process.argv.includes('--check-config')) { console.log('AgentCamp configuration and destination table valid'); return; }
  const server = await createApp(config, { gateway });
  let stopping = false;
  for (const signal of ['SIGTERM', 'SIGINT']) process.on(signal, () => {
    if (stopping) return;
    stopping = true;
    void server.close().then(() => process.exit(0));
  });
  await server.app.listen(config.AGENTCAMP_PORT, '127.0.0.1');
  console.log('AgentCamp API listening on loopback:' + config.AGENTCAMP_PORT);
}

if (require.main === module) void main().catch(() => { console.error('AgentCamp startup failed; check configuration and state directory'); process.exitCode = 1; });
