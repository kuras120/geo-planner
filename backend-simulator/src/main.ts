import { createContractSimulator, DEFAULT_HOST, DEFAULT_PORT } from './server.js';

const port = Number.parseInt(process.env['PORT'] ?? String(DEFAULT_PORT), 10);
if (!Number.isInteger(port) || port < 0 || port > 65_535) {
  throw new Error('PORT must be an integer from 0 to 65535.');
}

const server = createContractSimulator();

server.listen(port, DEFAULT_HOST, () => {
  console.log(`Geo Planner contract simulator listening on http://${DEFAULT_HOST}:${port}`);
});

for (const signal of ['SIGINT', 'SIGTERM'] as const) {
  process.on(signal, () => {
    server.close((error) => {
      if (error) {
        console.error('Failed to close the contract simulator cleanly.', error);
        process.exitCode = 1;
      }
    });
  });
}
