# Deploying to Streamlit Community Cloud

Order matters: the organisation must exist **before** you connect Streamlit, or
the OAuth prompt will not offer organisation access and you will have to
disconnect and start again.

## 1. Create the repository

In the `celnicconsulting` organisation, create a **public** repository named
`cities`. Do not initialise it with a README — this build already has one.

Then, from this folder:

```bash
git remote add origin https://github.com/celnicconsulting/cities.git
git push -u origin main
```

The repository is already initialised and committed, so `git init` is not needed.

The data file is 10 MB, well under GitHub's 50 MB warning threshold, so Git LFS is not required.

## 2. Deploy

1. Go to https://share.streamlit.io and sign in with GitHub
2. At the OAuth prompt, grant **organisation access** to `celnicconsulting`
3. Click **Create app**, then choose the existing repository
4. Set:
   - Repository: `celnicconsulting/cities`
   - Branch: `main`
   - Main file path: `app/cities.py`
   - **Custom subdomain**: `celnic-cities`

   Streamlit subdomains allow lowercase letters, digits and hyphens only — no
   underscores — so the URL uses hyphens even though the repository name uses
   underscores. That gives:

   **https://celnic-cities.streamlit.app/**
5. Deploy

The first build takes a few minutes while dependencies install.

To change the subdomain after deployment: the app's ⋮ menu → Settings → App URL
on share.streamlit.io.

## 3. After deploying

Put the live URL in `README.md` where it says _add your Streamlit URL here_.

## Resource envelope

Community Cloud allows up to 2.7 GB memory, 2 CPU cores and 50 GB storage. This
app opens a 10 MB DuckDB file read-only and caches query results, so it sits
well inside those limits. The heaviest query is the Data Explorer detail table,
which filters a 279,640-row fact — well under a second, and cached after the
first call.

## Updating the data later

The pipeline lives in the parent project, not in this repository. To refresh:

```bash
python scripts/run_all.py
```

Then copy the rebuilt extract and app into this folder and push:

```bash
cp public/cities_public.duckdb public_repo/data/
cp app/cities.py public_repo/app/
cp app/cities__readme.md public_repo/app/
git commit -am "Refresh data extract" && git push
```

Community Cloud redeploys automatically on push to the tracked branch.

The app keys its DuckDB connection on the extract's size and modified time, so a
redeploy picks up the new file without a manual reboot. Community Cloud does not
clear `cache_resource` on a hot reload, and without that fingerprint a connection
opened before the pull keeps reading the replaced file.

**Before refreshing, harvest a `catalogue.data.govt.nz` session cookie.** The
data.govt.nz download endpoints sit behind Imperva and return an 854-byte
challenge stub with HTTP 403 to any scripted request, curl included. The
catalogue *API* is open; only the file downloads are challenged. Load a dataset
page in a real browser, reload once so the challenge clears, copy the
`incap_ses_*` cookie from `document.cookie` into
`scripts/.cookies/catalogue.data.govt.nz.txt`, and start the download run
immediately — the cookie expired within about ten minutes on this build. The
pipeline raises rather than storing a stub as data, so a stale cookie fails
loudly instead of writing plausible rubbish.

The primary source on `hud.govt.nz` needs no cookie.
