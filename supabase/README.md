# Live catalog setup

The public site stays on GitHub Pages and Jekyll, but the staff editor now treats Supabase as the live catalog database.

## Architecture

- staff sign in with Supabase email/password accounts
- record edits save into `public.catalog_records`
- the editor can request a publish step after save
- the publish function exports the current Supabase catalog snapshot to `_data/africanart_mdl_medata.csv` in GitHub
- the commit to `main` triggers the normal GitHub Pages rebuild

## Required setup

1. Run [`supabase/schema.sql`](./schema.sql) in the Supabase SQL editor.
2. Run [`supabase/catalog_records_seed.sql`](./catalog_records_seed.sql) once to seed the live catalog from the current CSV snapshot.
3. Deploy the Edge Function from [`supabase/functions/catalog-writeback/index.ts`](./functions/catalog-writeback/index.ts).
4. Set these function secrets:
   - `GITHUB_TOKEN`
   - `GITHUB_REPO`
   - `GITHUB_BRANCH`
   - `GITHUB_CSV_PATH`
5. Invite staff users through Supabase Auth.

## Required site config

Set these values in `_data/theme.yml`:

- `editor-supabase-url`
- `editor-supabase-anon-key`
- `editor-supabase-table`
- `editor-writeback-endpoint`

## Operational model

- Supabase is the live editable catalog.
- `_data/africanart_mdl_medata.csv` is the published site snapshot.
- Staff can keep working in Supabase even if the publish step is temporarily unavailable.
