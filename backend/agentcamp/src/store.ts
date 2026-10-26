import { createHash, randomUUID } from 'node:crypto';
import { mkdirSync, chmodSync } from 'node:fs';
import { dirname } from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { Application } from './config';

export interface Submission {
  id: string;
  hash: string;
  payload: string | null;
  created_at: number;
  record_id: string | null;
  notified_at: number | null;
  attempts: number;
  next_attempt: number;
  lease_until: number;
  lease_owner: string | null;
}

export class SubmissionConflict extends Error {}

export class Store {
  private db: DatabaseSync;

  constructor(path: string, private now = Date.now) {
    if (path !== ':memory:') mkdirSync(dirname(path), { recursive: true, mode: 0o700 });
    this.db = new DatabaseSync(path, { timeout: 5000 });
    if (path !== ':memory:') chmodSync(path, 0o600);
    this.db.exec(`
      PRAGMA journal_mode=WAL;
      PRAGMA synchronous=FULL;
      CREATE TABLE IF NOT EXISTS submissions (
        id TEXT PRIMARY KEY, hash TEXT NOT NULL, payload TEXT,
        created_at INTEGER NOT NULL, record_id TEXT, notified_at INTEGER,
        attempts INTEGER NOT NULL DEFAULT 0, next_attempt INTEGER NOT NULL DEFAULT 0,
        lease_until INTEGER NOT NULL DEFAULT 0, lease_owner TEXT
      ) STRICT;
      CREATE INDEX IF NOT EXISTS submissions_hash ON submissions(hash, created_at);
      CREATE INDEX IF NOT EXISTS submissions_due ON submissions(next_attempt) WHERE notified_at IS NULL;
    `);
  }

  get(id: string): Submission | undefined {
    return this.db.prepare('SELECT * FROM submissions WHERE id = ?').get(id) as Submission | undefined;
  }

  accept(id: string, payload: Application): Submission {
    const encoded = JSON.stringify(payload);
    const hash = createHash('sha256').update(encoded).digest('hex');
    this.db.exec('BEGIN IMMEDIATE');
    try {
      const existing = this.get(id);
      if (existing && existing.hash !== hash) throw new SubmissionConflict();
      const duplicate = existing || this.db.prepare('SELECT * FROM submissions WHERE hash = ? AND created_at >= ? ORDER BY created_at DESC LIMIT 1')
        .get(hash, this.now() - 86400000) as Submission | undefined;
      if (duplicate) {
        this.db.exec('COMMIT');
        return duplicate;
      }
      this.db.prepare('INSERT INTO submissions(id, hash, payload, created_at) VALUES (?, ?, ?, ?)').run(id, hash, encoded, this.now());
      this.db.exec('COMMIT');
      return this.get(id)!;
    } catch (error) {
      this.db.exec('ROLLBACK');
      throw error;
    }
  }

  claim(id: string): Submission | undefined {
    return this.db.prepare(`UPDATE submissions SET lease_until = ?, lease_owner = ?
      WHERE id = ? AND notified_at IS NULL AND lease_until <= ? AND next_attempt <= ? RETURNING *`)
      .get(this.now() + 120000, randomUUID(), id, this.now(), this.now()) as Submission | undefined;
  }

  stored(row: Submission, recordId: string): void {
    this.db.prepare(`UPDATE submissions SET record_id = ?, attempts = 0, next_attempt = 0,
      lease_until = 0, lease_owner = NULL WHERE id = ? AND lease_owner = ?`)
      .run(recordId, row.id, row.lease_owner);
  }

  notified(row: Submission): void {
    // After delivery only retain the hash and identifiers needed for deduplication.
    this.db.prepare(`UPDATE submissions SET notified_at = ?, payload = NULL, attempts = 0,
      lease_until = 0, lease_owner = NULL WHERE id = ? AND lease_owner = ?`)
      .run(this.now(), row.id, row.lease_owner);
  }

  retry(row: Submission): void {
    const delay = Math.min(3600000, 10000 * 2 ** Math.min(row.attempts, 9));
    this.db.prepare(`UPDATE submissions SET attempts = attempts + 1, next_attempt = ?, lease_until = 0,
      lease_owner = NULL WHERE id = ? AND lease_owner = ?`).run(this.now() + delay, row.id, row.lease_owner);
  }

  due(): Submission[] {
    return this.db.prepare(`SELECT * FROM submissions WHERE notified_at IS NULL AND next_attempt <= ?
      AND lease_until <= ? ORDER BY next_attempt, created_at LIMIT 10`).all(this.now(), this.now()) as unknown as Submission[];
  }

  close(): void { this.db.close(); }
}
