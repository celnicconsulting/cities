# Flipping the Data Team — example driving from business outcome

The usual order is to model the data first and hope a useful application falls
out of it. This platform was built the other way round: the application spec came
first, and the transformation layer was designed to serve it.

Each tab was reduced to the single question it has to answer, and each question
to the grain that answers it. Only then was a mart table written — and a table
that no question needed was not built at all.

**Built from public releases by the Ministry of Housing and Urban Development,
whose functions moved to the Ministry for Cities, Environment, Regions and
Transport on 1 July 2026.** All 10 reconciliation checks pass. The published
extract is 10.2 MB.

**Deployment:** **live** at <https://celnic-cities.streamlit.app>.

---

# ====================THE_QUESTIONS_CAME_FIRST====================

| Tab | Question | Grain required | Mart table built |
|---|---|---|---|
| 📊 National Overview | What have house prices and sales done, nationally and by region? | series × month | `M_HPI_NATIONAL`, `M_HPI_REGION` |
| 🗺️ Price Map | Where are prices highest and rising fastest? | district, latest month | `M_HPI_TA_LATEST` |
| 💰 Area Explorer | How does one district compare, and does the value quartile change the story? | series × month × area × value quartile | `M_HPI_AREA`, `M_HPI_QUARTILE`, `M_SALES_AREA` |
| 📋 Data Explorer | Let me take the detail away | the fact, filtered | `M_HPI_QUARTILE` |
| ⚙️ Pipeline | Can I trust any of this? | file, check, lineage | `META_*`, `VALIDATION_RESULTS` |

**What that analysis forced into the design**, working back from the questions:

1. Every tab needs a **period, a place and a measure**, so the facts share one
   conformed shape — `PERIOD` as `YYYY-MM`, area names canonicalised, one measure
   column — rather than mirroring the publisher's worksheet.
2. Every tab also needs a **statistical series**, which was not obvious until the
   data was in hand. The source publishes `Monthly` and `3-Month rolling` in one
   sheet. They are two methodologies, not two periods, so the series became a
   first-class axis on every fact and a sidebar control rather than a hidden
   default.
3. The map needs **coordinates the publisher never provides**, so the design
   forced a bundled district geography and an explicit statement on the map that
   position is derived while price is measured.
4. The value-quartile tab needs the index cut by property value quartile — a
   split no other New Zealand house price index publishes — so the quartile
   dimension is carried whole rather than filtered to `All` at staging.
5. **Nothing needed synthetic data.** The published record turned out deep enough
   that every question could be answered from measured figures, so this platform
   has no `SYN` schema at all.

Note what is absent: no table was built because it was interesting, and no chart
was designed around a table that already existed.

---

# ====================WHAT_THE_BRIEF_GOT_WRONG====================

The research brief was written from search results before any data was in hand.
Five of its assumptions did not survive contact with the files. That gap is the
point of doing the research and the build as separate steps.

**The organisation had ceased to exist.** MCERT was created on 1 July 2026 by
merging the Ministry for the Environment, the Ministry of Housing and Urban
Development, the Ministry of Transport and the local government functions of the
Department of Internal Affairs. Every series in this platform crosses a
machinery-of-government boundary two months before it was built.

**The largest catalogue was not a statistics catalogue.** The Ministry for the
Environment lists 1,138 packages, which reads like the richest source available.
Its 7,475 resources are dominated by SHP, MapInfo, GPKG, OpenFileGDB, KML and
GeoTIFF — the same spatial layer republished seven or eight times — against 760
CSV. Sizing the build on the package count would have overstated the tabular
content by an order of magnitude.

**The history was longer than advertised.** The brief recorded the index as
starting in 1980, from the publisher's own announcement. Nationally it starts in
**1970**.

**Four proposed synthetic tables were all unnecessary.** The brief specified
property-level sales, household affordability, a vehicle fleet and a geography
bridge. Sales counts and quartile prices are published monthly at district grain
back to 1980, so generating property rows would have replaced measured data with
modelled data. The geography bridge became real reference data. The vehicle table
depended on a source that had to be cut.

**"It is an embedded dashboard" was not by itself a reason to cut a series.**
Two kinds of embed appear here with opposite outcomes. A Power BI report exports
nothing — but the underlying workbook is published on a different page, which is
the only reason this platform exists. A Tableau *worksheet* exports clean CSV
through a query parameter. A Tableau *story* returns HTTP 200 with a zero-byte
body, which is worse than an error because a pipeline will write the empty file
and carry on.

---

# ====================THREE_WAYS_A_PARSER_LIED====================

Each produced a result that looked entirely plausible. None was caught by
inspection; all three were caught by counting things.

**The filter that ate the headline.** Commentary sheets — Contents, Notes, Cover
— are skipped by name. Matching those words as substrings silently dropped the
sheet called **House Price Index**, because it contains the word "Index". The two
surviving sheets loaded cleanly, reconciled against themselves, and produced a
working platform missing its entire reason for existing. What exposed it was
adding up the rows and comparing them with the source workbook: 905,359 landed
against 1,184,999 published. The filter now matches whole sheet names only.

**The two series wearing one name.** The source publishes `Monthly` and
`3-Month rolling` in the same sheet, distinguished by a column that staging
dropped. Every chart still rendered. Every series simply had twice as many points
as it should, alternating between two different methodologies, and the national
index appeared to have 3,354 monthly observations in a 56-year series that can
only contain about 670. Counting periods per series is what exposed it.

**The macron that hid ten districts.** MCERT publishes district names in correct
te reo — Kāpiti Coast, Whangārei, Ōpōtiki, Taupō, Manawatū, Waipā, Whakatāne,
Ōtorohanga, Kaikōura — and calls the largest district "Auckland City". The
reference geography, reused from an older build, uses unmacronised spellings.
Joining on the raw label dropped exactly those ten districts. Every surviving
district still carried the right price, every total still reconciled, and the map
showed 44 districts in a country that has 67. Counting districts is what exposed
it. Every remapping is now recorded in a table the Pipeline tab displays.

The common thread: all three were invisible to any check that compared a number
against another number from the same code path. What caught them was counting
sheets, counting periods, and counting districts.

---

# ====================STAGING_AND_MART====================

The primary source lands **tidy** — `stat_type, area_type, area, period, …`
already in long format — so this build needs no header-inference machinery, no
cell-grid resolvers and no PDF geometry parsing for it. That is unusual for
government publications and it is why the whole platform is small.

Staging therefore does four things rather than parsing:

- **Types, keeping suppression as NULL.** 40,009 quartile prices are blank
  because the district had too few sales to publish. Read as zero they would be
  free houses dragging every average down.
- **Carries the statistical series** so nothing can group across the two.
- **Canonicalises area names before any join**, recording every substitution.
- **Takes one vintage.** The workbook is recalculated every month, so storage is
  keyed on a hash of the source URL and each month's download lands beside the
  last. Staging reads the newest and records which one, because two vintages are
  two estimates of the same 56 years — differencing them turns revisions into
  price movements.

The mart is seven tables in contract order, tab 1 first. The only derived thing
in the platform is map **position**.

---

# ====================VALIDATION====================

Ten checks, all passing, written to a table the application displays rather than
asserts. Four are **shape** checks, and they are there because shape is what
caught every real defect in this build:

| Check | What it would catch |
|---|---|
| primary source sheets landed | the substring filter that ate the index |
| districts unmatched to geography | the macron mismatch |
| districts published | a join quietly dropping a third of the country |
| statistical series kept apart | the two methodologies interleaving |
| suppressed prices held as NULL | an unpublished quartile read as a free house |
| national index within the regional range | a cross-check through a different aggregation |
| map rows carry coordinates | a district plotted at (0, 0) |

---

# ====================WHAT_WAS_LEFT_OUT====================

Two sources were registered and deliberately not ingested. Both appear in the
Pipeline tab with their reasons, because a source that quietly did not appear
would be indistinguishable from one that was never considered.

**Transport.** The statistics site sits behind a bot-protection product whose
session cookie expired within about ten minutes of being harvested, so the source
cannot run unattended. Its statistics index is also rendered in the browser
rather than in the HTML, so a plain crawl returns a single link and reports
success — the worst kind of failure. And the quarterly fleet series is a Tableau
story, which exports an empty file.

**Environment.** The catalogue is a spatial-data mirror rather than a statistics
catalogue, and nothing in it shares a grain with the housing series without a
scoping pass this build has not done.

---

# ====================RUNNING_IT====================

```bash
python scripts/01_discover.py    # crawl sources, emit the discovery manifest
python scripts/02_download.py    # download, keyed on a hash of the source URL
python scripts/03_extract.py     # to parquet: tidy where tidy, cell grids otherwise
python scripts/04_load_duckdb.py # build the RAW layer and its metadata
python scripts/05_stage.py       # resolve RAW into tidy staging facts
python scripts/07_mart.py        # conformed marts, in contract order
python scripts/06_validate.py    # reconciliation checks; non-zero exit on failure
python scripts/09_build_public.py# the extract the published app reads
```

Downloads are cached by local path and the databases are rebuilt from scratch
each load, so re-running is safe. Two hosts need a browser-harvested session
cookie stored before the crawl; the pipeline raises rather than storing a
challenge stub as data, so a stale cookie fails loudly instead of writing
plausible rubbish.
