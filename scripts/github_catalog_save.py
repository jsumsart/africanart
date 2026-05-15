#!/usr/bin/env python3

import csv
import json
import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
METADATA_PATH = ROOT / "_data" / "africanart_mdl_medata.csv"
THEME_PATH = ROOT / "_data" / "theme.yml"

ALLOWED_THEME_KEYS = {
    "primary_color": "primary-color",
    "secondary_color": "secondary-color",
    "text_color": "text-color",
    "link_color": "link-color",
    "body_font_family": "base-font-family",
    "heading_font_family": "heading-font-family",
    "featured_image": "featured-image",
    "home_banner_image_position": "home-banner-image-position",
}


def read_csv_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def write_csv_rows(path: Path, headers, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in headers})


def yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def replace_yaml_key(text: str, key: str, value: str) -> str:
    pattern = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
    replacement = f"{key}: {yaml_quote(value)}"
    if pattern.search(text):
        return pattern.sub(replacement, text)
    if not text.endswith("\n"):
        text += "\n"
    return text + replacement + "\n"


def apply_record_update(record_payload: dict):
    headers, rows = read_csv_rows(METADATA_PATH)
    object_name = (record_payload.get("Object name") or "").strip()
    if not object_name:
        raise ValueError("Record payload is missing 'Object name'.")

    target = None
    for row in rows:
        if row.get("Object name") == object_name:
            target = row
            break

    if target is None:
        raise ValueError(f"Record '{object_name}' was not found in the metadata CSV.")

    for header in headers:
        if header in record_payload:
            value = record_payload.get(header, "")
            target[header] = "" if value is None else str(value)

    write_csv_rows(METADATA_PATH, headers, rows)


def apply_settings_update(settings_payload: dict):
    theme_text = THEME_PATH.read_text(encoding="utf-8")
    for payload_key, theme_key in ALLOWED_THEME_KEYS.items():
        if payload_key in settings_payload:
            theme_text = replace_yaml_key(theme_text, theme_key, str(settings_payload.get(payload_key, "")))
    THEME_PATH.write_text(theme_text, encoding="utf-8")


def main():
    action_type = os.environ.get("SAVE_ACTION_TYPE", "").strip()
    record_json = os.environ.get("SAVE_RECORD_JSON", "").strip()
    settings_json = os.environ.get("SAVE_SETTINGS_JSON", "").strip()

    if action_type == "record":
        if not record_json:
            raise ValueError("SAVE_RECORD_JSON is required for record saves.")
        apply_record_update(json.loads(record_json))
        return

    if action_type == "settings":
        if not settings_json:
            raise ValueError("SAVE_SETTINGS_JSON is required for site settings saves.")
        apply_settings_update(json.loads(settings_json))
        return

    raise ValueError("SAVE_ACTION_TYPE must be 'record' or 'settings'.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # pragma: no cover
        print(str(error), file=sys.stderr)
        sys.exit(1)
