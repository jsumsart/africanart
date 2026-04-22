create table if not exists public.catalog_edit_audit (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default timezone('utc', now()),
  user_id uuid not null references auth.users(id) on delete cascade,
  user_email text,
  object_name text not null,
  commit_message text not null,
  commit_sha text,
  payload jsonb not null default '{}'::jsonb
);

alter table public.catalog_edit_audit enable row level security;

drop policy if exists "catalog audit insert by authenticated user" on public.catalog_edit_audit;
create policy "catalog audit insert by authenticated user"
on public.catalog_edit_audit
for insert
to authenticated
with check (auth.uid() = user_id);

drop policy if exists "catalog audit read own entries" on public.catalog_edit_audit;
create policy "catalog audit read own entries"
on public.catalog_edit_audit
for select
to authenticated
using (auth.uid() = user_id);
