import { Gateway, UpstreamError } from './feishu';
import { Store, Submission } from './store';

export class Service {
  private timer?: NodeJS.Timeout;
  private running?: Promise<void>;

  constructor(readonly store: Store, private gateway: Gateway) {}

  async deliver(id: string): Promise<Submission> {
    const current = this.store.get(id)!;
    if (current.record_id) return current;
    const row = this.store.claim(id);
    if (!row) return current;
    try {
      const recordId = await this.gateway.ensureRecord(row);
      this.store.stored(row, recordId);
    } catch (error) {
      this.store.retry(row);
      this.report(row, 'record', error);
    }
    return this.store.get(id)!;
  }

  private report(row: Submission, phase: string, error: unknown): void {
    console.error(JSON.stringify({ event: 'agentcamp_retry', id: row.id, phase,
      code: error instanceof UpstreamError ? error.code : 'internal' }));
  }

  async tick(): Promise<void> {
    if (this.running) return this.running;
    this.running = (async () => {
      for (const due of this.store.due()) {
        if (!due.record_id) { await this.deliver(due.id); continue; }
        const row = this.store.claim(due.id);
        if (!row) continue;
        try { await this.gateway.notify(row); this.store.notified(row); }
        catch (error) { this.store.retry(row); this.report(row, 'notification', error); }
      }
    })().finally(() => { this.running = undefined; });
    return this.running;
  }

  start(): void {
    this.timer = setInterval(() => {
      void this.tick().catch(() => console.error('{"event":"agentcamp_worker_error"}'));
    }, 5000);
    this.timer.unref();
  }

  async stop(): Promise<void> {
    clearInterval(this.timer);
    await this.running;
  }
}
