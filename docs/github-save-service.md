# Catalog Room GitHub Save Service

The public site stays on GitHub Pages, but Catalog Room needs one private save trigger so staff do not have to paste a GitHub token into the browser.

## What is already in the repository

- `/.github/workflows/catalog-room-save.yml`
  A GitHub Actions workflow that can save either:
  - one record into `/_data/africanart_mdl_medata.csv`
  - site-wide presentation settings into `/_data/theme.yml`

- `/scripts/github_catalog_save.py`
  The helper script that applies those payloads inside the repo before the workflow commits and pushes them back to `main`.

## GitHub secret required

Add this repository secret:

- `PAGES_PUSH_TOKEN`

Use a GitHub personal access token or GitHub App token with repository `Contents: Read and write` on `jsumsart/africanart`.

This secret is used by the workflow to push changes back to `main` so GitHub Pages rebuilds automatically.

## Netlify option now included in the repo

This repository now includes a ready-to-deploy Netlify Function:

- `/netlify/functions/catalog-room-save.js`
- `/netlify.toml`

That function:

1. receives a save request from Catalog Room
2. verifies the shared editor password on the server
3. calls the GitHub `workflow_dispatch` API for `catalog-room-save.yml`
4. passes the payload through as:
   - `save_action_type`
   - `editor_email`
   - `commit_message`
   - `record_json` or `settings_json`

## Netlify environment variables required

Add these in the Netlify project:

- `EDITOR_PASSWORD_SHA256`
  Use the same SHA-256 hash already stored in `/_data/theme.yml` for the Catalog Room password.
- `GITHUB_WORKFLOW_TOKEN`
  A GitHub token with permission to dispatch the workflow in `jsumsart/africanart`.
- `GITHUB_OWNER`
  `jsumsart`
- `GITHUB_REPO`
  `africanart`
- `GITHUB_WORKFLOW_ID`
  `catalog-room-save.yml`
- `GITHUB_WORKFLOW_REF`
  `main`

## Recommended request shape to the Netlify function

POST to:

- `/.netlify/functions/catalog-room-save`

## Recommended request shapes

### Record save

```json
{
  "editor_email": "student@jsums.edu",
  "editor_password": "JSUAfricanArt2026",
  "save_action_type": "record",
  "commit_message": "Save coll003 metadata",
  "record": {
    "Object name": "coll003",
    "Identifier": "JA-2006-01",
    "Title": "Tabwa Mask"
  }
}
```

### Site settings save

```json
{
  "editor_email": "student@jsums.edu",
  "editor_password": "JSUAfricanArt2026",
  "save_action_type": "settings",
  "settings": {
    "primary_color": "#14213d",
    "secondary_color": "#243b63",
    "featured_image": "coll032"
  }
}
```

## Why this is the right split

- GitHub keeps the source of truth
- GitHub Pages still publishes the site
- staff keep the simple shared Catalog Room sign-in
- browser users do **not** need a personal GitHub token
- the only private credential lives in one server-side place
