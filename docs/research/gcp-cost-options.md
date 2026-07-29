# GCP Cost Options

## Status

Initial cost research recorded on 2026-07-28 from official GCP/Firebase, Neon,
and Supabase pricing and product documentation. Prices vary by region,
currency, edition, traffic, and future provider changes. Recalculate against
the selected providers' current calculators before provisioning or accepting a
hosted plan.

This research compares development operating models; it does not authorize
resource creation.

## Cost Drivers

| Component | Billing shape | Geo Planner consequence |
| --- | --- | --- |
| Cloud Run | Requests, CPU, memory, and networking; can scale to zero | Good for intermittent API traffic if minimum instances remain zero. |
| Cloud SQL PostgreSQL | Running instance compute/memory plus storage, backups, IP, and network | Main baseline development cost; stopping suspends instance charges but storage and IP charges continue. |
| Firestore | Document/index reads, writes, deletes, storage, and network | Cheap for very small prototypes/free quota, but query shape and document modeling affect cost and architecture. |
| Cloud Storage | Stored bytes, operations, retrieval/class changes, and network egress | Raster retention and user delivery can dominate SaaS cost. |
| Firebase Hosting/CDN | Stored and transferred frontend assets | Usually small compared with map artifacts. |
| Firebase Authentication/Identity Platform | MAU and provider type; phone/SMS separately | Tier-1 providers currently have a substantial no-cost MAU tier; enterprise federation and SMS differ. |
| Acquisition compute | Cloud Run service/job time, temporary storage, outbound provider traffic | Depends on AOI, layers, resolution, retries, validation, and conversion/overview work. |

Official current free-tier evidence includes:

- Cloud Run: 240,000 vCPU-seconds and 450,000 GiB-seconds per month before
  location/egress qualifications;
- Firestore: one free database with 1 GiB stored, 50,000 document reads/day,
  20,000 writes/day, 20,000 deletes/day, and 10 GiB outbound/month;
- Identity Platform tier-1 authentication: 50,000 MAU before paid MAU tiers.

Free tiers are not architectural guarantees and do not replace budgets or
quotas.

## Development Profiles

### Profile L — Fully Local Daily Development (Recommended)

```text
Angular + Node simulator
Spring Boot
PostgreSQL container/Testcontainers
local .geo-planner-data/
Firebase emulators only for accepted auth/storage slices
```

- Cloud runtime cost: effectively zero.
- Highest development speed and deterministic offline tests.
- Same PostgreSQL semantics can later run in Cloud SQL.
- Does not test IAM, Cloud Run connection behavior, real Cloud Storage, or
  deployment packaging continuously.

Infrastructure code can still be developed, validated, and reviewed without
keeping resources running.

### Profile P — On-demand GCP Preview/Integration (Recommended Companion)

```text
Firebase Hosting/Auth
Cloud Run min instances = 0
Cloud SQL started only for integration windows
small Cloud Storage bucket with lifecycle cleanup
```

- Cloud Run can scale to zero between requests.
- Stop Cloud SQL after a session; compute charges pause, while storage and IP
  charges remain.
- Keep one small non-HA database, bounded storage, one Cloud Run instance
  maximum, and short artifact retention.
- Suitable for manual integration, owner review, demos, and periodic E2E.
- Startup/teardown automation and health checks are required to avoid forgotten
  resources and confusing cold starts.

### Profile C — Continuously Running Cloud Development

- Closest to hosted production topology.
- Cloud SQL, stored artifacts, logs, IP, and backups create a monthly baseline
  even with little product usage.
- Useful only when several collaborators or automated environments need
  continuous access.
- Not justified for the current single-owner discovery/MVP stage.

### Firestore-first Cost Variant

Firestore's free quota and emulator can make a tiny cloud prototype inexpensive
and remove always-on relational compute. The trade is architectural: document
reads become billable operations, a document is limited to 1 MiB, and later
relational/spatial requirements may force a migration. Treat this as a separate
product decision, not a free Cloud SQL substitute.

### External Managed PostgreSQL Variant

The application database does not have to run in GCP. Spring Boot on Cloud Run
can use an ordinary TLS PostgreSQL connection to an external managed service
while large artifacts remain in Cloud Storage.

This avoids Cloud SQL's continuously provisioned development compute without
changing the relational schema or requiring Firestore-specific persistence.
It introduces cross-provider internet traffic, another operational dependency,
and potentially higher query latency. Cloud Run outbound internet transfer is
billable after the applicable free allowance, whereas traffic to Google Cloud
resources in the same region can be free. The database must therefore contain
metadata and geometry, not raster bytes, and the selected database region
should be as close as practical to the Cloud Run region.

| Option | Development cost shape | Geo Planner fit | Main constraint |
| --- | --- | --- | --- |
| Neon PostgreSQL | Compute scales to zero after inactivity; current free plan includes 100 CU-hours and 0.5 GB per project | Strong candidate for intermittent development; standard PostgreSQL, PostGIS, pooling, and branches | Cold start, public cross-cloud connection, provider limits, and session behavior under scale-to-zero/transaction pooling |
| Supabase PostgreSQL | Current free plan includes two active projects, 500 MB database, and 5 GB egress; inactive free projects pause | Viable when its Auth, Storage, API, or admin UI will also be used | Duplicates planned Firebase services; paid projects do not pause and start from a standing subscription |
| Cloud SQL PostgreSQL | Provisioned instance; stopping suspends instance compute but retains some storage/network costs | Tightest GCP integration and simplest same-provider production path | Highest idle development baseline among these candidates |

Neon is the leading external-database candidate for this project because its
usage-based scale-to-zero model matches intermittent single-owner development
and keeps the application on PostgreSQL/PostGIS. Use the pooled TLS endpoint
with a small application-side pool; transaction pooling does not preserve
session-level features such as `LISTEN`, session advisory locks, or temporary
table state across transactions. Schema migrations and administrative tasks may
require a direct connection.

Supabase is technically suitable and explicitly supports PostGIS, but adopting
it only as a database while retaining Firebase Hosting/Auth and Cloud Storage
would pay for and operate overlapping platform capabilities. Reconsider it if
the product deliberately replaces Firebase services with the Supabase platform.

An external provider is not a permanent lock-in decision when the application:

- uses standard PostgreSQL migrations and portable PostGIS features;
- keeps provider SDKs outside the domain and persistence model;
- stores secrets in deployment configuration;
- tests migrations against local PostgreSQL;
- periodically proves `pg_dump`/restore into another PostgreSQL instance;
- keeps raster and export objects outside database columns.

## Workload Model

Before selecting a hosted profile, estimate monthly:

| Input | Symbol |
| --- | --- |
| active users | `U` |
| projects created per user | `P` |
| acquired raster GiB per project before retention cleanup | `A` |
| average retained fraction after lifecycle/deduplication | `R` |
| average browser transfer GiB per project view | `V` |
| project views per month | `Q` |
| acquisition compute seconds per project | `T` |
| database running hours per month | `H` |
| API-to-database transfer GiB per month | `D` |
| average API-to-database round trips per request | `N` |

Core quantities:

```text
retained GiB       = U × P × A × R
viewer egress GiB  = U × Q × V
acquisition time   = U × P × T
database baseline  = selected instance hourly price × H
external DB network = provider egress + Cloud Run internet egress for D
```

Add storage operations, retrieval/class-transition charges, backups, logging,
Cloud Run memory, and database/network costs using the selected region's
current price list. `N` is primarily a latency and connection-pressure input:
measure representative use cases rather than estimating cross-cloud behavior
from geographic distance alone.

Do not assume cross-user tile deduplication in the baseline. Measure it and
apply it only as a reduction to `R`.

## Cost Controls From The First GCP Project

- Separate development and production GCP projects and billing views.
- Use Infrastructure as Code; default to no persistent development deployment.
- Set Cloud Run minimum instances to zero and a low maximum-instance cap.
- Keep services, database, and bucket in one selected region where possible.
- Use a non-HA development database; no replicas or commitments.
- Bound Cloud SQL connection pools and Cloud Run maximum instances together.
- Apply development bucket lifecycle rules and abort incomplete uploads.
- Enforce product quotas for AOI, pixels, response bytes, retained bytes, and
  active jobs.
- Cap log retention/verbosity and never log artifact or overlay bodies.
- Add billing budgets and multiple alert thresholds. Budgets notify; they do
  not automatically cap spend.
- Add service quotas or an explicitly reviewed automated response when a hard
  cost brake is required.
- Label resources by environment, owner, and expiry; periodically report
  unlabeled or expired resources.

## Recommendation

Use Profile L for daily work and prepare Profile P as repeatable
Infrastructure-as-Code. Do not keep Cloud SQL running continuously during early
single-owner development. Provision/start the cloud database only when the
persisted-project slice needs real integration, then stop or destroy the
development environment after the review window.

Keep PostgreSQL as the functional recommendation, but decouple it from Cloud
SQL. For the first intermittent cloud development environment, evaluate Neon
PostgreSQL in an EU region as the leading candidate while retaining local
PostgreSQL for daily work. Cloud SQL remains the conservative same-provider
choice once continuous production load, private networking, support, or GCP
operational simplicity justifies its baseline.

Before provisioning, fill the workload model and compare:

1. local PostgreSQL + on-demand Cloud SQL;
2. local PostgreSQL + external scale-to-zero PostgreSQL;
3. Firestore-first plus expected migration cost;
4. file/embedded local persistence plus expected migration cost.

Run a short disposable proof before accepting an external provider: migrations,
PostGIS enablement, Cloud Run TLS connection and pooling, cold-start behavior,
backup/export and restore, measured latency, and cost/usage reporting. Do not
place real owner data in the proof.

## Primary References

- `https://cloud.google.com/run/pricing`
- `https://cloud.google.com/sql/pricing/`
- `https://docs.cloud.google.com/sql/docs/postgres/start-stop-restart-instance`
- `https://firebase.google.com/docs/firestore/pricing`
- `https://firebase.google.com/docs/firestore/quotas`
- `https://cloud.google.com/storage/pricing`
- `https://docs.cloud.google.com/storage/docs/lifecycle`
- `https://cloud.google.com/identity-platform/pricing`
- `https://docs.cloud.google.com/billing/docs/how-to/budgets`
- `https://neon.com/pricing`
- `https://neon.com/docs/introduction/scale-to-zero`
- `https://neon.com/docs/connect/connection-pooling`
- `https://neon.com/docs/reference/compatibility`
- `https://supabase.com/pricing`
- `https://supabase.com/docs/guides/platform/free-project-pausing`
- `https://supabase.com/docs/guides/platform/regions`
- `https://supabase.com/docs/guides/database/extensions`
