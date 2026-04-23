#!/usr/bin/env python3
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "_data" / "africanart_mdl_medata.csv"
OUTPUT = ROOT / "supabase" / "catalog_records_seed.sql"


def sql_escape(value: str) -> str:
    return value.replace("'", "''")


def to_sql_text(value: str) -> str:
    if value is None:
        return "null"
    return f"'{sql_escape(value)}'"


def main() -> None:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    statements = [
        "-- Generated from _data/africanart_mdl_medata.csv",
        "-- Run this after supabase/schema.sql to seed the live catalog table.",
        "",
    ]

    for row in rows:
        record_json = json.dumps(row, ensure_ascii=False).replace("'", "''")
        object_name = row.get("Object name", "")
        title = row.get("Title", "")
        culture = row.get("culture_community", "")
        location = row.get("Geographic location", "")
        file_name = row.get("File name", "")
        asset_format = row.get("format", "")

        statements.append(
            "insert into public.catalog_records "
            "(object_name, title, culture_community, geographic_location, file_name, asset_format, record) "
            f"values ({to_sql_text(object_name)}, {to_sql_text(title)}, {to_sql_text(culture)}, "
            f"{to_sql_text(location)}, {to_sql_text(file_name)}, {to_sql_text(asset_format)}, "
            f"'{record_json}'::jsonb) "
            "on conflict (object_name) do update set "
            "title = excluded.title, "
            "culture_community = excluded.culture_community, "
            "geographic_location = excluded.geographic_location, "
            "file_name = excluded.file_name, "
            "asset_format = excluded.asset_format, "
            "record = excluded.record;"
        )

    OUTPUT.write_text("\n".join(statements) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
