# Geo Planner Angular Frontend

This Angular workspace is the migration foundation for the replacement thin
client. It currently exposes only an accessible placeholder shell; the legacy
map remains the functional user interface.

The root application follows the Angular CLI `src/` convention. Reusable
libraries live under `projects/`:

- `ui` contains shared presentation primitives and their Storybook stories;
- `geo-planner-api` reserves generated transport, mapper, and facade boundaries
  for accepted backend contracts.

## Commands

From the repository root, install the pinned toolchain and locked dependencies:

```bash
mise install
mise run install
```

From `frontend/`:

```bash
npm start
npm run storybook
npm run test:unit
npm run e2e
npm run verify
```

`npm run api:generate -- <openapi-file>` generates a TypeScript Angular client
only from a supplied backend specification. Generated files are never
hand-edited. Whether generated sources are committed is decided with the first
accepted contract slice.

Runtime deployment configuration is read from `public/runtime-config.json`.
`apiBaseUrl` must remain a same-origin absolute path.

The Angular persistent disk cache is disabled because the current transitive
LMDB/message-pack native acceleration crashes under the pinned Node 24 build on
macOS ARM. This affects build speed only and can be revisited after the
dependency is corrected.
