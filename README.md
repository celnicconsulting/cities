# MCERT House Price Explorer

A Streamlit application over New Zealand's **MCERT House Price Index** and
property sales statistics — monthly, back to **1970**, at national, regional,
territorial authority and Auckland local board grain, cut by property value
quartile.

> **Data & licence.** Built on open data used under CC BY 4.0 — see
> [ATTRIBUTION.md](ATTRIBUTION.md) and [DATA_SOURCES.yaml](DATA_SOURCES.yaml)
> for every source, licence, and modification. Demonstration of method only:
> the data is modified, and must not be relied on for
> operational, policy, or reporting purposes.

**Live app:** _add your Streamlit URL here_

> ⚠️ **Built from New Zealand government data — not an official government
> product.** Figures are reproduced from public releases by the Ministry of
> Housing and Urban Development (including the MCERT House Price Index). This
> application is produced independently by Celnic Consulting and does not
> represent the views, policy or official statistics of those departments. Every
> original source file, with its download date and checksum, is listed in the
> app's ⚙️ Pipeline tab.

---

## What it shows

| Tab | Question it answers |
|---|---|
| 📊 National Overview | What have house prices and sales done, nationally and by region? |
| 🗺️ Price Map | Where are prices highest and rising fastest? |
| 💰 Area Explorer | How does one district compare, and does the value quartile change the story? |
| 📋 Data Explorer | Give me the detail, filtered, as a spreadsheet |
| ⚙️ Pipeline | Can I trust any of this? |
| 📓 Build Notes | How the platform was built, driven from the business outcome |

## Source and licence

Published by the **Ministry of Housing and Urban Development** (Te Tūāpapa Kura
Kāinga), whose functions transferred to the **Ministry for Cities, Environment,
Regions and Transport** on 1 July 2026. Recorded as **CC BY 4.0** — see
[ATTRIBUTION.md](ATTRIBUTION.md), which flags that the licence is assumed from
a build default and has not been verified against the publisher's terms.

Primary source: the Property and Sales Statistics workbook, published alongside
the [Property and Sales Statistics dashboard](https://www.hud.govt.nz/stats-and-insights/property-and-sales-statistics/about-the-dashboard),
with its methodology paper.

## Three things worth knowing about the data

**The whole series is recalculated every month.** Two vintages of this workbook
are two estimates of the same 56 years, not an old series plus new rows.
Differencing across vintages turns revisions into price movements. The vintage
in use is shown in the sidebar.

**Two statistics share one sheet.** The source publishes `Monthly` and
`3-Month rolling` figures together. They are different methodologies, not
different periods, and are never mixed here — the sidebar selects between them.
The default is 3-month rolling, because at the latest period the monthly index
covers 41 districts and the rolling one covers 61.

**Annual change is published nearly two years behind the index.** The headline
metric shows the latest period it actually exists for, and says which.

## Data provenance

All figures are **measured** from published releases. There is no synthetic data
in this application. The one derived element is map *position*: districts are
drawn on bundled centroids because the publisher releases area names without
coordinates, and the map says so.

## Running locally

```bash
pip install -r requirements.txt
streamlit run app/cities.py
```

The app reads `data/cities_public.duckdb` (10 MB) read-only.

## Rebuilding the data

The pipeline lives in the parent project, not in this repository. See
`DEPLOY.md` for the refresh procedure.

## Licence

Two licences apply, and they cover different things.

- **Code** — MIT. See [`LICENSE`](LICENSE). Covers the application, its helper
  modules and the build scripts.
- **Data** — the publishers' own terms, recorded per dataset. See
  [`LICENSE-DATA`](LICENSE-DATA) for the notice,
  [`DATA_SOURCES.yaml`](DATA_SOURCES.yaml) for the full manifest (publisher,
  URL, licence, retrieval date, modifications) and
  [`ATTRIBUTION.md`](ATTRIBUTION.md) for the reader-facing summary.

Source data is recorded as CC BY 4.0, but that value is a build default rather
than a verified fact — see the "Licence to confirm" section of
[`ATTRIBUTION.md`](ATTRIBUTION.md) before redistributing it.
