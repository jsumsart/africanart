create table if not exists public.catalog_records (
  object_name text primary key,
  title text,
  culture_community text,
  geographic_location text,
  file_name text,
  asset_format text,
  record jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default timezone('utc', now()),
  updated_at timestamptz not null default timezone('utc', now()),
  updated_by uuid references auth.users(id) on delete set null
);

create or replace function public.set_catalog_records_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = timezone('utc', now());
  return new;
end;
$$;

drop trigger if exists set_catalog_records_updated_at on public.catalog_records;
create trigger set_catalog_records_updated_at
before update on public.catalog_records
for each row
execute function public.set_catalog_records_updated_at();

alter table public.catalog_records enable row level security;

drop policy if exists "catalog records readable by authenticated users" on public.catalog_records;
create policy "catalog records readable by authenticated users"
on public.catalog_records
for select
to authenticated
using (true);

drop policy if exists "catalog records insert by authenticated users" on public.catalog_records;
create policy "catalog records insert by authenticated users"
on public.catalog_records
for insert
to authenticated
with check (auth.uid() is not null);

create table if not exists public.site_settings (
  id integer primary key default 1 check (id = 1),
  primary_color text,
  secondary_color text,
  text_color text,
  link_color text,
  body_font_family text,
  heading_font_family text,
  featured_image text,
  home_banner_image_position text,
  created_at timestamptz not null default timezone('utc', now()),
  updated_at timestamptz not null default timezone('utc', now()),
  updated_by uuid references auth.users(id) on delete set null
);

create or replace function public.set_site_settings_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = timezone('utc', now());
  return new;
end;
$$;

drop trigger if exists set_site_settings_updated_at on public.site_settings;
create trigger set_site_settings_updated_at
before update on public.site_settings
for each row
execute function public.set_site_settings_updated_at();

alter table public.site_settings enable row level security;

drop policy if exists "site settings readable by all users" on public.site_settings;
create policy "site settings readable by all users"
on public.site_settings
for select
to anon, authenticated
using (true);

drop policy if exists "site settings insert by authenticated users" on public.site_settings;
create policy "site settings insert by authenticated users"
on public.site_settings
for insert
to authenticated
with check (auth.uid() is not null and id = 1);

drop policy if exists "site settings update by authenticated users" on public.site_settings;
create policy "site settings update by authenticated users"
on public.site_settings
for update
to authenticated
using (auth.uid() is not null and id = 1)
with check (auth.uid() is not null and id = 1);

drop policy if exists "catalog records update by authenticated users" on public.catalog_records;
create policy "catalog records update by authenticated users"
on public.catalog_records
for update
to authenticated
using (auth.uid() is not null)
with check (auth.uid() is not null);

create table if not exists public.catalog_edit_audit (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default timezone('utc', now()),
  user_id uuid not null references auth.users(id) on delete cascade,
  user_email text,
  object_name text not null,
  save_message text not null,
  publish_sha text,
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
