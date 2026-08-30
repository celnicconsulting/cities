# Attribution

This repository demonstrates a data-platform build method. It is **not**
an official publication of any agency named below, and no agency has
endorsed it. Data has been **modified** (downloaded, staged and
transformed) — treat every figure as untrusted demonstration output.

This platform contains **no synthetic data**. Every figure in the published
extract is measured from a public release; the only derived element is map
*position*, which uses bundled district centroids because the publisher
releases area names without coordinates.

## Source datasets

### Ministry of Housing and Urban Development (Te Tūāpapa Kura Kāinga)

Functions transferred to the Ministry for Cities, Environment, Regions and
Transport (MCERT) on 1 July 2026. Data still publishes under the predecessor
brand and domain.

| Dataset | Publisher | Licence | Source |
|---|---|---|---|
| Property and Sales Statistics (including the MCERT House Price Index) | Ministry of Housing and Urban Development | ⚠️ CC BY 4.0 *(to confirm)* | [about the dashboard](https://www.hud.govt.nz/stats-and-insights/property-and-sales-statistics/about-the-dashboard) |
| Ministry of Housing and Urban Development catalogue on data.govt.nz | Ministry of Housing and Urban Development, via data.govt.nz | ⚠️ CC BY 4.0 *(to confirm)* | [CKAN package search](https://catalogue.data.govt.nz/api/3/action/package_search?fq=organization:ministry-of-housing-and-urban-development&rows=100) |

Both were retrieved on **27 August 2026**. Only the first supplies figures the
app charts; the second contributes build metadata only (download manifest and
RAW table summary), shown in the app's ⚙️ Pipeline tab.

## Licence to confirm

Both rows above are marked ⚠️ because the licence is **recorded but not
verified**:

- The `CC BY 4.0` value is the dataclass default in `scripts/org_sources.py`.
  No source entry overrides it, so the value carried through the shipped
  `META_SOURCE_REGISTER` table is assumed, not checked.
- The only licence evidence the build actually captured for
  `hud.govt.nz` is the saved page footer — `© 2026 Te Tūāpapa Kura Kāinga —
  Ministry of Housing and Urban Development`, linking to a "Copyright and
  disclaimer" page that was never fetched. New Zealand agency releases are
  usually CC BY 4.0 under NZGOAL, but that is not on record here.
- For the data.govt.nz catalogue, licence is a **per-package** question across
  27 packages. CKAN returns a `licence_id` per package; discovery did not
  capture it, so none of the 27 licences is recorded. Several landed packages
  are Household Economic Survey derivatives carrying Stats NZ suppression and
  randomised rounding, which may attach further conditions of use.

Neither finding is evidence that the data is *not* CC BY 4.0 — it is that the
build never checked. Recommended action: fetch the hud.govt.nz copyright page
and re-run discovery capturing `licence_id` per CKAN package, then set an
explicit `licence` on each `Source` in `scripts/org_sources.py` so the value is
recorded rather than defaulted. Full detail is in
[DATA_SOURCES.yaml](DATA_SOURCES.yaml).

## Sources registered but not used

`META_SOURCE_REGISTER` ships four further sources so the Pipeline tab can show
what was left out and why. **No data from them appears in this repository** and
they are not attributed as datasets: Housing statistics and insights
(hud.govt.nz, nothing landed), Ministry of Transport statistics (blocked by a
short-lived Imperva cookie; the quarterly fleet series is a Tableau story that
exports a zero-byte body), Ministry for the Environment catalogue (a
spatial-data mirror, not a statistics catalogue), and DIA local government
(scope undetermined).

---

Source data © the named publishers, used under CC BY 4.0
(https://creativecommons.org/licenses/by/4.0/) subject to the confirmation
noted above. Attribution does not imply endorsement.
