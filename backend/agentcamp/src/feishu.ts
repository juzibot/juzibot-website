import { Application, Config } from './config';
import { Submission } from './store';

export class UpstreamError extends Error {
  constructor(public readonly code: string) { super('Feishu request failed'); }
}

export interface Gateway {
  ensureRecord(row: Submission): Promise<string>;
  notify(row: Submission): Promise<void>;
}

export class Feishu implements Gateway {
  private token = '';
  private expires = 0;
  private tokenRequest?: Promise<string>;

  constructor(private config: Config, private fetcher: typeof fetch = fetch) {}

  private async request(path: string, body?: unknown, authenticated = true): Promise<any> {
    const token = authenticated ? await this.getToken() : '';
    let response: Response;
    let result: any;
    try {
      response = await this.fetcher('https://open.feishu.cn/open-apis' + path, {
        method: body === undefined ? 'GET' : 'POST',
        headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: 'Bearer ' + token } : {}) },
        body: body === undefined ? undefined : JSON.stringify(body),
        signal: AbortSignal.timeout(8000),
        redirect: 'error'
      });
      result = await response.json();
    } catch { throw new UpstreamError('network'); }
    if (!response.ok || result.code !== 0) {
      if ([99991663, 99991668].includes(result.code)) this.expires = 0;
      throw new UpstreamError(String(result.code || response.status));
    }
    return result;
  }

  private async getToken(): Promise<string> {
    if (this.token && Date.now() < this.expires) return this.token;
    if (!this.tokenRequest) {
      this.tokenRequest = (async () => {
        const r = await this.request('/auth/v3/tenant_access_token/internal', {
          app_id: this.config.AGENTCAMP_APP_ID, app_secret: this.config.AGENTCAMP_APP_SECRET
        }, false);
        if (typeof r.tenant_access_token !== 'string' || !(r.expire > 60)) throw new UpstreamError('invalid_token_response');
        this.token = r.tenant_access_token;
        this.expires = Date.now() + (r.expire - 60) * 1000;
        return this.token;
      })().finally(() => { this.tokenRequest = undefined; });
    }
    return this.tokenRequest;
  }

  private get recordsPath(): string {
    return '/bitable/v1/apps/' + this.config.AGENTCAMP_BASE_TOKEN + '/tables/' + this.config.AGENTCAMP_TABLE_ID + '/records';
  }

  async verifyDestination(): Promise<void> {
    const path = this.recordsPath.replace(/\/records$/, '');
    let page = '';
    let tableFound = false;
    do {
      const tables = await this.request('/bitable/v1/apps/' + this.config.AGENTCAMP_BASE_TOKEN + '/tables?page_size=100' + (page ? '&page_token=' + encodeURIComponent(page) : ''));
      const table = tables.data?.items?.find((item: any) => item.table_id === this.config.AGENTCAMP_TABLE_ID);
      if (table) {
        const expected = this.config.AGENTCAMP_ENV === 'production' ? 'AgentCamp 线索' : 'AgentCamp 线索（测试）';
        if (table.name !== expected) throw new UpstreamError('wrong_destination_table');
        tableFound = true;
        break;
      }
      page = tables.data?.has_more ? tables.data.page_token : '';
    } while (page);
    if (!tableFound) throw new UpstreamError('destination_not_found');
    const required: Record<string, number> = {
      '提交编号': 1, '姓名': 1, '公司': 1, '职位': 1, '手机或邮箱': 1, '城市': 1,
      '期望时间': 1, '想做的业务': 1, '数据准备情况': 1, '来源': 1, '来源页面': 1,
      '同意联系': 7, '提交时间': 5, '状态': 3, '跟进人': 11, '跟进备注': 1, '环境': 3
    };
    const found: Record<string, number> = {};
    page = '';
    do {
      const fields = await this.request(path + '/fields?page_size=100' + (page ? '&page_token=' + encodeURIComponent(page) : ''));
      for (const field of fields.data?.items || []) found[field.field_name] = field.type;
      page = fields.data?.has_more ? fields.data.page_token : '';
    } while (page);
    if (Object.entries(required).some(([name, type]) => found[name] !== type)) throw new UpstreamError('destination_schema_mismatch');
    // Bot membership is checked by sending during delivery; never send a startup message.
  }

  async ensureRecord(row: Submission): Promise<string> {
    // Recover a committed remote write after a lost response or a process restart.
    const search = await this.request(this.recordsPath + '/search?page_size=2', {
      field_names: ['提交编号'],
      filter: { conjunction: 'and', conditions: [{ field_name: '提交编号', operator: 'is', value: [row.id] }] }
    });
    if (!Array.isArray(search.data?.items)) throw new UpstreamError('invalid_search_response');
    if (search.data.items.length) {
      const id = search.data.items[0].record_id;
      if (typeof id !== 'string') throw new UpstreamError('invalid_record_response');
      return id;
    }
    const p = JSON.parse(row.payload!) as Application;
    const result = await this.request(this.recordsPath + '?client_token=' + row.id, {
      fields: {
        '提交编号': row.id, '姓名': p.name, '公司': p.company, '职位': p.title,
        '手机或邮箱': p.contact, '城市': p.city, '期望时间': p.when,
        '想做的业务': p.task, '数据准备情况': p.data, '来源': 'AgentCamp',
        '来源页面': 'agentcamp.html', '同意联系': true, '提交时间': row.created_at,
        '状态': '待跟进', '环境': this.config.AGENTCAMP_ENV
      }
    });
    if (typeof result.data?.record?.record_id !== 'string') throw new UpstreamError('invalid_record_response');
    return result.data.record.record_id;
  }

  recordUrl(recordId: string): string {
    const url = new URL(this.config.AGENTCAMP_BASE_URL);
    url.searchParams.set('table', this.config.AGENTCAMP_TABLE_ID);
    url.searchParams.set('record', recordId);
    return url.href;
  }

  async notify(row: Submission): Promise<void> {
    const p = JSON.parse(row.payload!) as Application;
    const singleLine = (s: string, max: number) => s.replace(/\s+/g, ' ').replace(/</g, '＜').replace(/>/g, '＞').slice(0, max);
    const text = [
      (this.config.AGENTCAMP_ENV === 'preview' ? '【预览测试】' : '') + 'AgentCamp 新报名',
      '公司：' + singleLine(p.company, 200), '姓名：' + singleLine(p.name, 80),
      '需求：' + singleLine(p.task, 300), '提交编号：' + row.id,
      '查看线索：' + this.recordUrl(row.record_id!)
    ].join('\n');
    await this.request('/im/v1/messages?receive_id_type=chat_id', {
      receive_id: this.config.AGENTCAMP_CHAT_ID, msg_type: 'text',
      content: JSON.stringify({ text }), uuid: row.id
    });
  }
}
