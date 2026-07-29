# Geo Planner Backend Simulator

This loopback-only Node application is the frontend contract simulator. The
foundation exposes only `GET /_simulator/health`. Product routes, named
scenarios, payloads, and fixtures are added with accepted OpenAPI contract
slices; the simulator never defines the contract itself.

```bash
npm ci
npm run build
npm start
```

Run `npm run verify` for formatting, strict type checking, build, and tests.
