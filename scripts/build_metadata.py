#!/usr/bin/env python3

import csv
import re
from pathlib import Path


ROOT = Path("/Users/Birittany/Documents/African Art")
OBJECTS_DIR = ROOT / "objects"
DATA_DIR = ROOT / "_data"
MASTER_CSV = DATA_DIR / "africanart_mdl_medata.csv"
SITE_CSV = DATA_DIR / "africanart_metadata.csv"
SOURCE_CSV = Path(
    "/Users/Birittany/Downloads/Data  Jackson State University African Art Collection - Data  Jackson State University African Art Collection (1).csv"
)
MAX_OBJECT_ID = 148

MASTER_HEADERS = [
    "Object name",
    "Identifier",
    "Alternate ID",
    "Title",
    "Alternate title(s)",
    "Replaces",
    "Replaced by",
    "Description",
    "Creator",
    "Searchable date",
    "Date",
    "Coverage (time period)",
    "Time period",
    "Subject",
    "Mississippi county",
    "Geographic location",
    "Resource type",
    "Format",
    "Media format",
    "Language",
    "Language code",
    "Publisher",
    "Contributors",
    "Notes",
    "Rights",
    "Disclaimer",
    "Contributing institution",
    "Collection",
    "Source",
    "Digital repository",
    "Digital collection",
    "File size",
    "File extension",
    "Width",
    "Height",
    "Color space",
    "Date digital",
    "Capture method",
    "Processing software",
    "Master image",
    "Record created by",
    "Hidden notes",
    "Custom searches",
    "IP resolution",
    "Transcript",
    "File name",
    "culture_community",
    "people_ethnolinguistic_group",
    "place_of_creation",
    "place_of_use",
    "materials",
    "technique",
    "object_type",
    "function_use",
    "period_dynasty",
    "provenance",
    "acquisition_context",
    "preferred_term",
    "legacy_title",
    "attribution_confidence",
    "cultural_sensitivity_note",
    "youtubeid",
    "vimeoid",
    "latitude",
    "longitude",
    "format",
]


def natural_key(text: str):
    return [
        (0, int(part)) if part.isdigit() else (1, part.lower())
        for part in re.split(r"(\d+)", text)
        if part
    ]


def read_csv_rows(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, headers, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in headers})


def mime_type(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".png":
        return "image/png"
    if suffix == ".gif":
        return "image/gif"
    if suffix in {".tif", ".tiff"}:
        return "image/tiff"
    return ""


def clean_title_from_filename(filename: str) -> str:
    stem = Path(filename).stem.strip()
    stem = stem.replace("_", " ")
    stem = re.sub(r"(?<=\D)(\d+)$", r" \1", stem)
    stem = re.sub(r"\s+", " ", stem).strip()
    if stem.isdigit():
        return f"Untitled object {int(stem)}"
    return stem or filename


def build_objectid(index: int) -> str:
    return f"coll{index:03d}"


def legacy_index_by_filename():
    rows = read_csv_rows(SITE_CSV)
    return {row.get("filename", "").strip(): row for row in rows if row.get("filename")}


def source_index_by_objectid():
    rows = read_csv_rows(SOURCE_CSV)
    indexed = {}
    for row in rows:
        link = (row.get("Link") or "").strip()
        match = re.search(r"id=(coll\d+)", link)
        if match:
            indexed[match.group(1)] = row
    return indexed


def normalize_subjects(value: str) -> str:
    if not value:
        return ""
    parts = [part.strip() for part in value.split(",") if part.strip()]
    return "; ".join(parts)


def clean_source_title(value: str) -> str:
    text = (value or "").strip()
    if not text or text == "?":
        return ""
    if text.isdigit():
        return ""
    return text


def enrich_from_source(row, source_row):
    if not source_row:
        return row

    source_title = clean_source_title(source_row.get("Title", ""))
    tribal = (source_row.get("Tribal Affiliation") or "").strip()
    country = (source_row.get("Country") or "").strip()
    medium = (source_row.get("Medium") or "").strip()
    subjects = normalize_subjects(source_row.get("Subjects", ""))
    date_text = (source_row.get("Date") or "").strip()
    description = (source_row.get("Description") or "").strip()

    if source_title:
        row["Title"] = source_title
    if date_text and date_text != "?":
        row["Date"] = date_text
        row["Coverage (time period)"] = date_text
        row["period_dynasty"] = date_text
    if description and description != "placeholder":
        row["Description"] = description
    if tribal:
        row["culture_community"] = tribal
    if country:
        row["Geographic location"] = country
        row["place_of_creation"] = country
    if medium and medium != "n/a":
        row["materials"] = medium
    if subjects and subjects != "n/a":
        row["Subject"] = subjects

    return row


def sync_helper_fields(row):
    row["Object name"] = row.get("Object name", "") or row.get("Identifier", "")
    row["format"] = row.get("format", "") or mime_type(row.get("File name", ""))
    return row


def default_master_row(filename: str, index: int, legacy_row):
    objectid = build_objectid(index)
    title = clean_title_from_filename(filename)
    hidden_note = (
        "Scaffold record generated from the local object inventory. "
        "Review and replace provisional values during cataloging."
    )
    if title.startswith("Untitled object"):
        hidden_note += " Provisional title derived from numeric filename."
    else:
        hidden_note += " Provisional title derived from filename."

    source = ""
    if legacy_row:
        source = (legacy_row.get("source") or "").strip()

    return {
        "Object name": objectid,
        "Identifier": "",
        "Alternate ID": "",
        "Title": title,
        "Alternate title(s)": "",
        "Replaces": "",
        "Replaced by": "",
        "Description": (
            "From the Jackson State University African Art Collection. "
            "Detailed description pending cataloging review."
        ),
        "Creator": "Unknown",
        "Searchable date": "",
        "Date": "",
        "Coverage (time period)": "",
        "Time period": "",
        "Subject": "",
        "Mississippi county": "",
        "Geographic location": "",
        "Resource type": "Physical Object",
        "Format": "",
        "Media format": "Object",
        "Language": "",
        "Language code": "",
        "Publisher": "Jackson State University. (electronic version); JSUMS ART. (electronic version)",
        "Contributors": "",
        "Notes": "",
        "Rights": "IN COPYRIGHT; http://rightsstatements.org/vocab/InC/1.0/",
        "Disclaimer": (
            "All rights reserved. Reproduction or redistribution requires written permission "
            "from Jackson State University."
        ),
        "Contributing institution": "Jackson State University.",
        "Collection": "Jackson State University African Art Collection.",
        "Source": source,
        "Digital repository": "JSUMS ART.",
        "Digital collection": "African Art, Jackson State University.",
        "File size": "",
        "File extension": "",
        "Width": "",
        "Height": "",
        "Color space": "",
        "Date digital": "",
        "Capture method": "",
        "Processing software": "",
        "Master image": "",
        "Record created by": "",
        "Hidden notes": hidden_note,
        "Custom searches": "",
        "IP resolution": "",
        "Transcript": "",
        "File name": filename,
        "culture_community": "",
        "people_ethnolinguistic_group": "",
        "place_of_creation": "",
        "place_of_use": "",
        "materials": "",
        "technique": "",
        "object_type": "",
        "function_use": "",
        "period_dynasty": "",
        "provenance": "",
        "acquisition_context": "",
        "preferred_term": "",
        "legacy_title": "",
        "attribution_confidence": "",
        "cultural_sensitivity_note": "",
        "youtubeid": "",
        "vimeoid": "",
        "latitude": (legacy_row.get("latitude") or "").strip() if legacy_row else "",
        "longitude": (legacy_row.get("longitude") or "").strip() if legacy_row else "",
        "format": mime_type(filename),
    }


def load_or_seed_master():
    legacy = legacy_index_by_filename()
    source = source_index_by_objectid()
    files = sorted(
        [path.name for path in OBJECTS_DIR.iterdir() if path.is_file()],
        key=natural_key,
    )
    existing_rows = read_csv_rows(MASTER_CSV)
    rows_by_file = {
        row.get("File name", "").strip(): row
        for row in existing_rows
        if row.get("File name")
    }

    merged_rows = []
    for index, filename in enumerate(files, start=1):
        if index > MAX_OBJECT_ID:
            break
        existing = rows_by_file.get(filename)
        if existing:
            row = {header: existing.get(header, "") for header in MASTER_HEADERS}
            if not row.get("Object name"):
                row["Object name"] = row["Identifier"] or build_objectid(index)
            if not row.get("Title"):
                row["Title"] = clean_title_from_filename(filename)
            row["File name"] = filename
            row["youtubeid"] = row.get("youtubeid", "")
            row["vimeoid"] = row.get("vimeoid", "")
        else:
            row = default_master_row(filename, index, legacy.get(filename))
        if row.get("Identifier", "").startswith("JSU_AA_"):
            row["Identifier"] = ""
            row["Object name"] = row.get("Object name", "") or build_objectid(index)
        row = enrich_from_source(row, source.get(row.get("Object name", "")))
        row = sync_helper_fields(row)
        merged_rows.append(row)
    return merged_rows


def main():
    master_rows = load_or_seed_master()
    write_csv(MASTER_CSV, MASTER_HEADERS, master_rows)
    print(f"Wrote {len(master_rows)} master records to {MASTER_CSV}")


if __name__ == "__main__":
    main()
