import { strict as assert } from 'node:assert';
import { test } from 'node:test';

import { routeRequest } from './server.js';

test('reports simulator readiness without exposing a product endpoint', () => {
  const response = routeRequest('GET', '/_simulator/health', 'simulator-test');

  assert.equal(response.status, 200);
  assert.equal(response.contentType, 'application/json');
  assert.equal(response.correlationId, 'simulator-test');
  assert.deepEqual(response.body, {
    service: 'geo-planner-contract-simulator',
    status: 'ready',
  });
});

test('rejects routes that have no accepted contract fixture', () => {
  const response = routeRequest('GET', '/api/projects', 'simulator-test');

  assert.equal(response.status, 404);
  assert.equal(response.contentType, 'application/problem+json');
  assert.equal(response.body['title'], 'No simulated contract route');
});
