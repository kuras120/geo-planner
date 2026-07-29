import { randomUUID } from 'node:crypto';
import { createServer, type IncomingMessage, type Server, type ServerResponse } from 'node:http';

export const DEFAULT_HOST = '127.0.0.1';
export const DEFAULT_PORT = 4300;

const HEALTH_PATH = '/_simulator/health';

export interface SimulatorResponse {
  readonly body: Readonly<Record<string, unknown>>;
  readonly contentType: 'application/json' | 'application/problem+json';
  readonly correlationId: string;
  readonly status: number;
}

function correlationId(request: IncomingMessage): string {
  const requested = request.headers['x-correlation-id'];
  return typeof requested === 'string' && requested.length <= 128 ? requested : randomUUID();
}

export function routeRequest(
  method: string | undefined,
  requestUrl: string | undefined,
  requestCorrelationId: string,
): SimulatorResponse {
  const url = new URL(requestUrl ?? '/', `http://${DEFAULT_HOST}`);

  if (method === 'GET' && url.pathname === HEALTH_PATH) {
    return {
      body: {
        service: 'geo-planner-contract-simulator',
        status: 'ready',
      },
      contentType: 'application/json',
      correlationId: requestCorrelationId,
      status: 200,
    };
  }

  return {
    body: {
      type: 'about:blank',
      title: 'No simulated contract route',
      status: 404,
      detail:
        'Product routes are added only with an accepted OpenAPI contract slice and representative fixtures.',
    },
    contentType: 'application/problem+json',
    correlationId: requestCorrelationId,
    status: 404,
  };
}

function sendJson(response: ServerResponse, simulatorResponse: SimulatorResponse): void {
  const payload = JSON.stringify(simulatorResponse.body);

  response.writeHead(simulatorResponse.status, {
    'cache-control': 'no-store',
    'content-length': Buffer.byteLength(payload),
    'content-type': `${simulatorResponse.contentType}; charset=utf-8`,
    'x-correlation-id': simulatorResponse.correlationId,
  });
  response.end(payload);
}

export function createContractSimulator(): Server {
  return createServer((request, response) => {
    sendJson(response, routeRequest(request.method, request.url, correlationId(request)));
  });
}
