import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';

const [specification] = process.argv.slice(2);

if (!specification) {
  console.error('Usage: npm run api:generate -- <path-to-openapi-spec>');
  process.exit(2);
}

const input = resolve(specification);
if (!existsSync(input)) {
  console.error(`OpenAPI specification does not exist: ${input}`);
  process.exit(2);
}

const result = spawnSync(
  'openapi-generator-cli',
  [
    'generate',
    '--input-spec',
    input,
    '--generator-name',
    'typescript-angular',
    '--output',
    'projects/geo-planner-api/src/lib/generated',
    '--config',
    'openapi-generator-config.json',
  ],
  { stdio: 'inherit', shell: process.platform === 'win32' },
);

process.exit(result.status ?? 1);
