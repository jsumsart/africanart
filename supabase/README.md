# Staff write-back setup

This site keeps GitHub Pages and Jekyll for the public presentation layer while using Supabase for staff authentication and a small server-side write-back bridge.

## What this does

- staff sign in with Supabase email/password accounts from any device
- the Edge Function receives an authenticated request
- the function updates `_data/africanart_mdl_medata.csv` in GitHub
- the commit to `main` triggers the normal GitHub Pages rebuild
- the public site reflects the update after the Pages deploy finishes

## Required Supabase setup

1. Create a Supabase project.
2. Run [`supabase/schema.sql`](./schema.sql) in the SQL editor.
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
- `editor-writeback-endpoint`

The write-back endpoint should be the full HTTPS URL of the deployed `catalog-writeback` function.

## Notes

- The hidden password-based gates in the site still control access to the research tools and the editor UI.
- Supabase staff sign-in is the trusted layer that allows actual write-back.
- The editor still supports local drafts even when write-back is not configured.
