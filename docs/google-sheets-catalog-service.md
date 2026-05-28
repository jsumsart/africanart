# Catalog Room Google Sheets Service

The public site can remain on GitHub Pages while the live editing workspace writes to a shared Google Sheet. This avoids Netlify usage limits and lets multiple student workers update records in the same place.

## What this setup does

- `Catalog Room` loads records from a Google Sheet when the service is configured.
- `Catalog Room` saves updated record rows back into that sheet.
- `Site Settings` saves collection-wide presentation settings into a second sheet tab.
- `Export all records as MDL CSV` downloads the current live sheet data as a CSV export.

## Files already prepared in this repo

- `/google-apps-script/catalog_room_sheet_service.gs`
- `/_includes/js/catalog-editor.html`
- `/_includes/js/site-settings-editor.html`
- `/_data/theme.yml`

## Google Sheet structure

Create one spreadsheet with two tabs:

1. `catalog_records`
2. `site_settings`

### `catalog_records`

Import the current master catalog CSV:

- `/_data/africanart_mdl_medata.csv`

The first row must remain the header row.

### `site_settings`

Create a simple two-column sheet with this structure:

| key | value |
| --- | --- |
| primary_color | #14213d |
| secondary_color | #243b63 |
| text_color | #1b1a17 |
| link_color | #8f4b22 |
| body_font_family | 'Source Sans 3', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif |
| heading_font_family | 'Source Serif 4', Georgia, serif |
| featured_image | coll032 |
| home_banner_image_position | center |

## Apps Script setup

1. Open the spreadsheet.
2. Go to `Extensions` → `Apps Script`.
3. Replace the default script with the contents of:
   - `/google-apps-script/catalog_room_sheet_service.gs`
4. In `Project Settings`, add these script properties:
   - `EDITOR_PASSWORD_SHA256`
   - `SPREADSHEET_ID`
   - optional `RECORDS_SHEET_NAME` = `catalog_records`
   - optional `SETTINGS_SHEET_NAME` = `site_settings`
5. Deploy as a web app:
   - Execute as: `Me`
   - Who has access: `Anyone with the link`

## Theme configuration

After deployment, paste the web app URL into:

- `editor-save-endpoint`
- `editor-site-settings-endpoint`

in:

- `/_data/theme.yml`

## Endpoints used by the frontend

### GET `?action=bootstrap`

Returns:

```json
{
  "ok": true,
  "records": [ ... ],
  "settings": { ... }
}
```

### GET `?action=export_csv`

Returns the live `catalog_records` sheet as CSV text.

### POST record save

```json
{
  "editor_email": "student@jsums.edu",
  "editor_session_hash": "sha256-password-hash",
  "save_action_type": "record",
  "commit_message": "Optional note",
  "record": {
    "Object name": "coll003",
    "Identifier": "JA-2006-01",
    "Title": "Tabwa Mask"
  }
}
```

### POST site settings save

```json
{
  "editor_email": "student@jsums.edu",
  "editor_session_hash": "sha256-password-hash",
  "save_action_type": "settings",
  "settings": {
    "primary_color": "#14213d",
    "featured_image": "coll032"
  }
}
```

## Important note

This setup makes Google Sheets the working catalog. The public GitHub Pages site will not update automatically from each save. Use the live editing workspace during cataloging, then export the updated MDL CSV when you are ready to publish a refreshed site snapshot.
