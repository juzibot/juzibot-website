// Local QA only: the mock gateway never contacts Feishu or creates real leads.
const http = require('node:http');
const express = require('express');
const { resolve } = require('node:path');
const { createApp } = require('../dist/main');
const { readConfig } = require('../dist/config');

async function startPreview(port = 8086) {
  let writes = 0, notices = 0;
  const config = readConfig({
    AGENTCAMP_APP_ID: 'cli_test', AGENTCAMP_APP_SECRET: 'local-qa',
    AGENTCAMP_BASE_TOKEN: 'testbase', AGENTCAMP_TABLE_ID: 'tblTest', AGENTCAMP_CHAT_ID: 'oc_test',
    AGENTCAMP_BASE_URL: 'https://example.feishu.cn/base/testbase',
    AGENTCAMP_ORIGINS: `http://127.0.0.1:${port}`, AGENTCAMP_DB_PATH: ':memory:', AGENTCAMP_ENV: 'preview'
  });
  const gateway = { async ensureRecord() { writes++; return 'recLocal' + writes; }, async notify() { notices++; } };
  const api = await createApp(config, { gateway });
  await api.app.listen(0, '127.0.0.1');
  const apiPort = api.app.getHttpServer().address().port;
  const frontend = express();
  frontend.use('/api/agentcamp', (req, res) => {
    const upstream = http.request({ hostname: '127.0.0.1', port: apiPort, path: req.originalUrl,
      method: req.method, headers: req.headers }, response => {
      res.writeHead(response.statusCode, response.headers); response.pipe(res);
    });
    upstream.on('error', () => res.status(502).end());
    req.pipe(upstream);
  });
  frontend.get('/__qa/status', (_req, res) => res.json({ writes, notices }));
  frontend.use(express.static(resolve(__dirname, '../../..'), { dotfiles: 'deny' }));
  const web = frontend.listen(port, '127.0.0.1');
  await new Promise((resolve, reject) => { web.once('listening', resolve); web.once('error', reject); });
  return { close: async () => { await new Promise(resolve => web.close(resolve)); await api.close(); } };
}

module.exports = { startPreview };
if (require.main === module) startPreview().then(server => {
  console.log('Local QA preview: http://127.0.0.1:8086/agentcamp.html (mock data only)');
  for (const signal of ['SIGTERM', 'SIGINT']) process.on(signal, () => void server.close().then(() => process.exit(0)));
}).catch(error => { console.error(error.message); process.exitCode = 1; });
