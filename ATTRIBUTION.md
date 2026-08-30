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

Functions transferred to the **Ministry for Cities, Environment, Regions and
Transport** (MCERT) on 1 July 2026. MCERT is the current publisher. Data still
publishes under the predecessor brand and domain: `hud.govt.nz` still resolves
in its own right and has not been redirected to the MCERT domain.

| Dataset | Publisher | Licence | Basis | Evidence |
|---|---|---|---|---|
| Property and Sales Statistics (including the MCERT House Price Index) | MCERT, publishing as Te Tūāpapa Kura Kāinga — Ministry of Housing and Urban Development | **CC BY 4.0** † | Agency-wide statement | [Copyright and disclaimer](https://www.hud.govt.nz/about-us/copyright-and-disclaimer) |
| MHUD catalogue on data.govt.nz — 27 packages | Ministry of Housing and Urban Development, via data.govt.nz | **Not uniform** — 23 packages **CC BY 3.0 NZ**, 4 packages ⚠ **no licence stated** | Per-package catalogue record | [CKAN package search](https://catalogue.data.govt.nz/api/3/action/package_search?fq=organization:ministry-of-housing-and-urban-development&rows=100) |

† *Agency-level record: the licence was read from a site-wide statement, not
from a statement attached to this dataset. See [Licence basis](#licence-basis).*

⚠ *Unverified: no licence could be established from the source.*

Both were retrieved on **27 August 2026**; the licences above were verified at
source on **30 August 2026**. Only the first supplies figures the app charts;
the second contributes build metadata only (download manifest and RAW table
summary), shown in the app's ⚙️ Pipeline tab.

## Licence basis

Each licence is classified by how it was established:

- **`dataset_page`** — read from this dataset's own page or its own catalogue
  record.
- **`agency_record`** (marked †) — only an agency-wide or site-wide statement
  was found, nothing specific to this dataset.
- **`unverified`** (marked ⚠) — could not be established.

### Property and Sales Statistics — CC BY 4.0, agency record †

The dataset's own [about the dashboard](https://www.hud.govt.nz/stats-and-insights/property-and-sales-statistics/about-the-dashboard)
page states **no licence of its own** — only a general disclaimer and the
footer `© 2026 Te Tūāpapa Kura Kāinga - Ministry of Housing and Urban
Development`. That footer's "Copyright and disclaimer" link has now been
fetched. It states:

> "Crown Copyright © Te Tūāpapa Kura Kāinga - Ministry of Housing and Urban
> Development … this copyright material is licensed for re-use under a Creative
> Commons Attribution 4.0 International Licence. You are free to copy,
> distribute and adapt the material, as long as you attribute it to us and
> abide by other licence terms."

The grant **excludes** logos, emblems and trademarks, the site's design
elements, photography and imagery, and third-party material. None of those is
redistributed here — what ships is tabular figures derived from the published
workbook.

So `CC BY 4.0` is now a **checked fact**, where previously it was a build
default. It is still marked † because the statement is site-wide for
`hud.govt.nz`, not attached to this dataset.

The publisher's own disclaimer travels with the data: the information is for
general information purposes only and **must not be relied on for financial,
investment, valuation or other decision-making purposes**.

### The HUD → MCERT transition

Checked 30 August 2026:

- `hud.govt.nz` **still resolves** and has **not** redirected. Both the dataset
  page and the copyright page are live under that domain, carrying a banner:
  "On 1 July 2026, the Ministry of Housing and Urban Development is now part of
  the new Ministry for Cities, Environment, Regions and Transport."
- The successor's site exists at [www.mcert.govt.nz](https://www.mcert.govt.nz/),
  and its [copyright page](https://www.mcert.govt.nz/copyright/) states:
  > "Unless otherwise stated (either below or within specific items or
  > collections), this copyright material is licensed for re-use under a
  > Creative Commons Attribution 4.0 International Licence."

**The licence statement did not change at the transition.** Predecessor and
successor both assert CC BY 4.0 with the same logo, imagery and third-party
exclusions. Data retrieved on **27 August 2026** was retrieved from
`hud.govt.nz` after the 1 July transfer, so the operative statement is the
`hud.govt.nz` "Copyright and disclaimer" page as it stood on that date; the
MCERT statement is recorded as corroboration and is identical in substance.

### data.govt.nz catalogue — not uniform

Licence on a catalogue is a **per-package** question. All 27 package records
were read directly from CKAN, which returns a `license_id` per package:

| Licence | `license_id` | Packages | Basis |
|---|---|---|---|
| Creative Commons Attribution 3.0 New Zealand | `CC-BY-NZ-3.0` | 23 of 27 | dataset record |
| ⚠ No licence stated | *(empty)* | 4 of 27 | unverified |

Licence URL for the 23: <https://creativecommons.org/licenses/by/3.0/nz/>.

The four packages with **no licence stated** return an empty `license_id`, an
empty `license_title` and a null `license_url` — CKAN's "License not
specified". No licence is inferred for them:

- `hes-warm-dry-damp-mould-2021-ethnicity` — HES Warm and Dry / Damp or Mould 2021 by ethnicity
- `hes-tenure-ethnicity-2018-2021` — HES Tenure by Ethnicity 2018 – 2021
- `hes-lowest-quartile-and-quintile-household-income-gross-and-disposable` — HES: Lowest Quartile and Quintile Household Income
- `hes-property-ownership` — HES: Property Ownership

**This corrects a wrong value.** The previously recorded `CC BY 4.0` was the
dataclass default in `scripts/org_sources.py`. **No package on this catalogue
is CC BY 4.0**, and no single licence covers the organisation.

The CKAN organisation slug is **unchanged** by the MCERT transition —
`ministry-of-housing-and-urban-development` is still live and still returns 27
packages. There is no MCERT organisation on data.govt.nz.

*(Note: `organization_show` reports `package_count: 27` but returns only the
first 10 packages. `package_search` with `rows=100` returns all 27 and is the
authoritative read.)*

## Stats NZ conditions on the underlying statistics

**23 of the 27** catalogue packages are derived from Stats NZ collections — 17
from the **Household Economic Survey (HES)**, the rest from the Census of
Population and Dwellings or the Integrated Data Infrastructure. The Creative
Commons licence on the MHUD catalogue record does not displace the
confidentiality conditions Stats NZ applies to the underlying outputs under the
Statistics Act 1975:

- **Suppression** — cells based on fewer than five people or households are
  suppressed in released HES tables.
- **Random rounding (base three)** — counts are randomly rounded, so a
  published cell is **not an exact count** and small differences between cells
  are not meaningful.

Handling rules applied throughout this build, and required of anyone reusing
figures of this kind:

- Suppressed values are held as **NULL, never as zero**.
- Randomly rounded series are **never differenced**.
- **Total-response ethnicity** categories are never summed or differenced — a
  respondent may appear in more than one.

These conditions attach to the figures, not to the metadata. **None of these
figures is republished in this repository** — only the download manifest and
RAW table summary derived from the build.

## Sources registered but not used

`META_SOURCE_REGISTER` ships four further sources so the Pipeline tab can show
what was left out and why. **No data from them appears in this repository** and
they are not attributed as datasets: Housing statistics and insights
(hud.govt.nz, nothing landed), Ministry of Transport statistics (blocked by a
short-lived Imperva cookie; the quarterly fleet series is a Tableau story that
exports a zero-byte body), Ministry for the Environment catalogue (a
spatial-data mirror, not a statistics catalogue), and DIA local government
(scope undetermined).

The `CC BY 4.0` values shown against those four rows in the shipped
`META_SOURCE_REGISTER` table are still the **unverified dataclass default** —
that table is a build artefact and was not rebuilt by this verification pass.
No data from those sources ships, so nothing is redistributed under a wrong
licence, but the table's licence column should not be read as a check.

---

**Charted data** © Te Tūāpapa Kura Kāinga — Ministry of Housing and Urban
Development (now MCERT), used under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), modified.
**Catalogue metadata** © Ministry of Housing and Urban Development, 23 of 27
packages under [CC BY 3.0 NZ](https://creativecommons.org/licenses/by/3.0/nz/)
and 4 with no licence stated. Attribution does not imply endorsement. Full
manifest: [DATA_SOURCES.yaml](DATA_SOURCES.yaml).
