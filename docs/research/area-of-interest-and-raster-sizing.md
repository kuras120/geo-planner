# Area Of Interest And Raster Sizing

## Status

Discovery proposal recorded on 2026-07-28 from the owner workflow and current
prototype behavior. Provider-specific limits and default resolutions still
require validation before an API contract or requirement is accepted.

## User Need

A project may start from one parcel, several parcels, or another explicit
geometry, but the useful map normally includes surrounding context. The system
must derive a reproducible acquisition area and usable raster resolution
without asking the user to calculate a WMS bbox or pixel dimensions.

## Current Prototype

`project-config.json` independently hard-codes:

- a list of focus and context parcels;
- one bbox shared by all vector filtering and raster footprints;
- one width and height shared by every WMS raster.

Changing the parcel list does not recalculate the bbox. Changing the bbox does
not recalculate raster dimensions or refresh bound snapshots. The configured
960 × 1040 pixels over 480 × 520 metres happen to represent 0.5 m/px in each
direction, but that relationship is not expressed or validated.

The union envelope of the currently configured parcel sources is approximately
457 × 456 metres. Its configured bbox clips about 33 metres on the west and
12 metres on the south while adding about 56 metres east and 76 metres north.
This confirms that the bbox is neither a validated subject envelope nor a
consistent context buffer.

## Provider Metadata Check

Official capabilities were read without downloading map snapshots on
2026-07-28:

| Current service | Advertised image dimensions | Discovery consequence |
| --- | --- | --- |
| GUGiK ORTO WMS 1.3.0 | `MaxWidth=4096`, `MaxHeight=4096` | A request planner may use a lower product tile cap but must not exceed the advertised cap. |
| KIEG WMS 1.3.0 | `MaxWidth=4096`, `MaxHeight=4096` | Apply the exact descriptor/capabilities version used by the acquisition. |
| KIUT WMS 1.3.0 | `MaxWidth=4096`, `MaxHeight=4096` | Apply the exact descriptor/capabilities version used by the acquisition. |
| KINA WMS 1.1.1 | No maximum width/height advertised | Treat dimensions as unknown and use a conservative product cap until validated; never inherit another provider's limit. |

The ORTO catalog contains source datasets with different native ground sample
distances, including 0.25 and 0.5 metre pixels. Request resolution therefore
belongs to the selected layer/coverage descriptor rather than one universal
project value. ULDK documentation describes parcel lookup and aggregate-area
operations but does not publish a throughput budget; the product still needs
its own bounded parcel count, timeout, retry, and concurrency policy.

Official evidence:

- `https://mapy.geoportal.gov.pl/wss/service/PZGIK/ORTO/WMS/StandardResolution?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0`
- `https://integracja.gugik.gov.pl/cgi-bin/KrajowaIntegracjaEwidencjiGruntow?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0`
- `https://integracja.gugik.gov.pl/cgi-bin/KrajowaIntegracjaUzbrojeniaTerenu?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0`
- `https://mapy.geoportal.gov.pl/wss/ext/KrajowaIntegracjaNumeracjiAdresowej?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.1.1`
- `https://uldk.gugik.gov.pl/opis.html`
- `https://www.geoportal.gov.pl/pl/dane/ortofotomapa-orto/`

## Proposed Neutral Flow

1. Accept one or more full parcel identifiers, or an explicit polygon/bbox for
   expert and non-cadastral workflows.
2. Resolve every parcel to canonical geometry in an explicit project CRS.
3. Preserve the selected geometries and their union as the project subject.
4. Reject the subject when its union envelope exceeds server-owned maximum
   width, height, area, separation, or estimated acquisition budgets.
5. Derive an acquisition bbox from the valid union envelope plus a bounded context
   buffer.
6. Show the selected parcels, buffer, and resulting extent before acquisition;
   allow an intentional adjustment within product limits.
7. For each selected layer, choose an accepted ground resolution and derive
   raster pixel dimensions.
8. Split requests deterministically when provider dimension, pixel, area, or
   response-size limits would be exceeded.
9. Validate and promote all artifacts with their exact tile bbox, resolution,
   source identity, and acquisition record.

The context buffer must be explicit project input or a visible product default,
not an accidental margin hidden in a bbox. Selecting multiple parcels must not
silently add every neighboring parcel as a project subject; surrounding parcel
data may be fetched separately as display context.

The owner accepted a 100 metre context buffer as the visible project default on
2026-07-28. A user may deliberately choose any value from 0 to 500 metres. The
chosen value is persisted with the project and the resulting extent is shown
before acquisition. The allowed input range does not bypass hard AOI or
acquisition budgets: a large subject may be unable to use the full 500 metres.

The maximum AOI envelope is a backend safety boundary, not a confirmation
dialog. If selected parcels are so distant that the combined project would
exceed the hard span, area, pixel, byte, or request budget, resolution fails
before buffering and acquisition. The response identifies the incompatible
selection and directs the user to create separate projects. Neither expert bbox
input nor explicit user confirmation may bypass this boundary.

The owner accepted the initial local-MVP geometry profile on 2026-07-28:

- at most 2 kilometres of envelope width;
- at most 2 kilometres of envelope height;
- at most 4 square kilometres of envelope area;
- at most 100 selected parcels.

The backend applies the profile to the normalized subject before buffering and
again to the resulting acquisition extent. Exceeding it requires separate
projects. A deployment profile may raise these values only after explicit load,
storage, and provider validation; user confirmation never raises them.

## Raster Calculation

For an acquisition bbox `[minX, minY, maxX, maxY]` in a metric CRS and target
resolution `r` metres per pixel:

```text
widthPx  = ceil((maxX - minX) / r)
heightPx = ceil((maxY - minY) / r)
```

The system then applies the source descriptor's:

- supported CRS and axis order;
- minimum and maximum width/height;
- maximum total pixels, area, response bytes, and request rate;
- supported format and transparency;
- recommended or permitted resolution range.

If the derived request exceeds a limit, it is split into aligned tiles. The
system must not silently stretch a smaller image over the whole bbox or reduce
resolution below the accepted value. Different layers may require different
resolutions and limits even when they cover the same project area.

The owner accepted the initial local-MVP raster profile on 2026-07-28:

- 0.5 m/px default resolution;
- 0.25 m/px only for a smaller AOI whose selected source/coverage supports that
  detail;
- 1 m/px as an explicit lower-cost choice;
- 2048 × 2048 product tile dimensions even when a provider advertises 4096 ×
  4096;
- at most 16 million pixels per layer, 64 planned tile requests per
  acquisition, 64 MiB per response, and 512 MiB of promoted artifacts per
  acquisition.

The planner never silently coarsens resolution. It offers a smaller AOI,
smaller buffer, or explicit 1 m/px choice when a budget would be exceeded.

Large acquisition delivery is intentionally deferred to its backend vertical
slice, but its boundary is fixed: the backend streams response bodies into
bounded temporary storage, validates and atomically promotes artifacts, and
reports per-layer stages/progress. The frontend does not download the whole
acquisition into memory or embed it into an application document; it displays
progress and later consumes controlled artifact/tile endpoints.

## Important Edge Cases

| Condition | Required discovery outcome |
| --- | --- |
| Several adjacent parcels | One union subject and one buffered acquisition extent may be appropriate. |
| Several disconnected but nearby parcels within hard limits | Show the unused envelope/context area and allow a deliberate project decision. |
| Parcels whose combined envelope exceeds hard limits | Reject the AOI before buffering/acquisition; identify the conflict and require separate projects. No confirmation override. |
| Parcel lookup partly fails | Preserve resolved selections, identify failures, and do not acquire an ambiguous partial project without confirmation. |
| Source lacks the project CRS | Use an explicit accepted reprojection path or mark the layer unavailable; never guess axis order. |
| One raster tile fails | Keep the last complete artifact and report the failed/partial acquisition; do not promote a silently incomplete mosaic. |
| User requests excessive context or resolution | Show the limiting budget and offer a smaller extent, coarser accepted resolution, or multiple projects. |
| Layer has no data in the AOI | Report a valid no-data result separately from provider failure or unsupported coverage. |

## Candidate Requirements

After discovery gates are complete, evaluate at least:

- `Projects / AOI`: create a project area from one or more parcels with visible,
  adjustable surrounding context;
- `Layer acquisition`: derive bounded raster requests from the AOI and
  layer-specific ground resolution, using deterministic tiling when required.

These may remain separate requirements because selecting the subject area and
acquiring a particular source layer have different failure modes and acceptance
evidence.

## Open Decisions

- Whether a user adjusts the bbox directly or only the buffer/context geometry.
- How context parcels are selected and displayed without becoming project
  subjects.
