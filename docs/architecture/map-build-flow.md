# Map Build Flow

```mermaid
flowchart LR
    PC["project-config.json\nidentity + spatial/source config"]
    VC["map-config.json\npresentation"]
    SO["sources/\nparcel WKT + plan GML"]
    RA["assets/\nraster snapshots"]
    MT["manual-overlays.example.json\ntracked empty initializer"]
    MO["manual-overlays.json\nignored local user data"]
    UP["update_sources.py\nexplicit network refresh"]
    BU["build_map.py\nvalidate + parse + embed"]
    TM["map-fragment.template.html\nshared UI"]
    HT["configured standalone HTML"]
    ED["edit_map_server.py\nloopback persistence + hot reload"]

    PC --> UP
    UP --> SO
    UP --> RA
    MT --> MO
    PC --> BU
    VC --> BU
    SO --> BU
    RA --> BU
    MO --> BU
    TM --> BU
    BU --> HT
    ED --> BU
    ED --> MO
    HT --> ED
```

## Boundaries

- Refresh is the only normal workflow that calls external data services.
- Build is deterministic for the checked-in configuration, snapshots, template, and the current local overlays. A missing local overlay file is initialized from the tracked empty example.
- Generated HTML is ignored because it embeds current data, rasters, and potentially private local overlays. It loads `d3-geo` from a CDN.
- The editor serves only the map directory on loopback, validates writes, persists overlays atomically, rebuilds, and signals the browser to reload.
- Direct `file://` use cannot write the repository; it uses project-namespaced browser storage and supports export.
