# Market Opportunity Assessment

## Status And Decision Trace

- Evidence checked: 2026-07-19 from public market signals; no customer
  interviews or willingness-to-pay tests have been completed.
- Question: which value and paying workflow could differentiate Geo Planner
  from a parcel viewer after the accepted map MVP?
- Completed boundary: current requirements do not attempt to build a full
  GIS/CAD, automated legal analysis, land-register system, or national copy of
  public source data.
- Open decisions: primary paying segment, dominant repeated workflow, and the
  role of reports, interactive projects, and monitoring.
- Return before: expanding the product roadmap beyond accepted requirements,
  selecting a commercial offer, or treating a product hypothesis as strategy.

The direction below remains a hypothesis until supported by recent-process
interviews, manually delivered analyses, and observable willingness to pay.

## Findings

The need exists, but another layered parcel map is unlikely to be a durable
advantage. Geoportal, PLANIA, QGIS, and commercial report services can replace
parts of the viewing workflow. Project continuity, interpretable evidence,
private scenarios, and change monitoring appear harder to substitute.

Parcel analysis currently combines Geoportal, public-information portals,
planning documents, utility maps, and private material. Public sources expose
data but rarely guide a decision; professional GIS remains too complex for many
owners, agents, and small investors. Planning reform and standardized data also
reduce the defensibility of simple layer display.

## Product Hypothesis

The most promising direction is a digital parcel dossier:

```text
CHECK -> PLAN -> MONITOR
```

- **Check:** collect official data and expose sources, dates, uncertainty, and
  limitations.
- **Plan:** create non-binding building, access, or subdivision scenarios.
- **Monitor:** detect new documents and planning changes affecting an area.

## Existing Alternatives

The comparison assesses fit for the proposed workflow, not overall product
quality:

| Product | Primary strength | Gap relative to the hypothesis |
| --- | --- | --- |
| PLANIA | Parcels, drawing, measurements, GML/DXF, and export | Full source set and local-workspace behavior were not confirmed. |
| Geoportal.gov.pl | Current Polish official data and feature identification | Limited personal project continuity and scenario workflow. |
| QGIS with QField | Full GIS, formats, automation, and offline use | High learning and configuration cost for non-specialists. |
| Scribble Maps | Simple sketches and export | No built-in Polish official-source workflow. |
| Felt | Collaboration and modern map interaction | Cloud-first and no confirmed Polish integration set. |
| OnGeo and Działki360 | Automated parcel risks and reports | No confirmed private scenario editor or continuous project workspace. |
| Geoportal Krajowy / Na Mapie | Fast parcel search and selection | Weaker evidence-to-scenario-to-history workflow. |

PLANIA is the first practical comparator for sketching and GIS/CAD exchange.
QGIS/QField remain the professional spatial-system benchmark. Geoportal and
commercial reports can serve a one-time parcel check. A dedicated product is
justified only when continuity, selected source interpretation, private
scenarios, and simplicity outweigh integration maintenance.

## Candidate Users And Offers

| Segment | Repeated need | Plausible offer |
| --- | --- | --- |
| Small land investors | Portfolio comparison and monitoring | Subscription |
| Architects and advisers | Rapid analysis and client communication | Professional workspace |
| Land agents | Evidence-backed buyer communication | Subscription or report |
| Owners of larger sites | Access, utilities, subdivision, and plan changes | Project plus monitoring |
| One-time buyers | Check one parcel | Report or time-limited access |

| Hypothesis | Potential value | Main risk |
| --- | --- | --- |
| Create a project from parcel, address, or polygon | Removes manual source assembly | Uneven data quality and coverage |
| Explain parcel status | Interprets evidence instead of only displaying it | False appearance of legal certainty |
| Monitor documents and zones | Creates repeated value | Change detection across fragmented sources |
| Model development scenarios | Supports early decisions | Must not resemble surveying or construction design |
| Compare parcels | Supports an actual purchase choice | Requires comparable evidence |
| Export and share privately | Improves collaboration | Privacy and interpretation liability |

## Validation Before A Product Decision

Interview users about recent real processes, sources consulted, time and money
spent, feared errors, and repeated checks. Deliver several analyses manually
and test separate offers for a report, interactive project, and monitoring.
Behavior and payment are stronger evidence than opinions about a hypothetical
application. Automate only after a leading workflow and segment emerge.

## Risks And Limitations

- Missing data does not prove absence; coverage and currency vary.
- Conclusions need a source, date, confidence, and legal or surveying caveat.
- Public portals and report vendors may absorb basic presentation features.
- A one-off report alone rarely supports a long-term subscription.
- The public-source review does not replace customer or purchasing evidence.
- Competitor comparison used public descriptions, not complete tests of paid
  tiers, accounts, offline policies, or every export. Recheck current features,
  prices, and policies before positioning or purchasing decisions.

## Sources And Market Signals

- [MRiT — general-plan deadline](https://www.gov.pl/web/rozwoj-technologia/wydluzony-termin-sporzadzania-planow-ogolnych)
- [MRiT — spatial-planning reform](https://www.gov.pl/web/rozwoj-technologia/reforma-planowania-przestrzennego-2)
- [GUGiK — proposed general plans in Geoportal](https://www.gov.pl/web/gugik/projektowane-plany-ogolne-gmin-pog-w-serwisie-wwwgeoportalgovpl)
- [General-plan data standard](https://www.gov.pl/web/zagospodarowanieprzestrzenne/szybki-start--pog)
- [OnGeo](https://ongeo.pl/)
- [Działki360](https://www.dzialki360.pl/)
- [Parcela AI](https://zanda.eu/)
- [AnalizaChlonnosci.ai](https://analizachlonnosci.ai/)
- [PLANIA](https://plania.pl/)
- [QGIS](https://qgis.org/) and [QField](https://qfield.org/)
- [Scribble Maps](https://www.scribblemaps.com/)
- [Felt](https://felt.com/)
- [Geoportal Krajowy](https://geoportal-krajowy.pl/)

These sources indicate market activity and increasing data availability. They
do not establish a target segment, willingness to pay, or product-market fit.
