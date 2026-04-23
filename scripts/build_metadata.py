#!/usr/bin/env python3

import csv
import re
import subprocess
from pathlib import Path


ROOT = Path("/Users/Birittany/Documents/African Art")
OBJECTS_DIR = ROOT / "objects"
DATA_DIR = ROOT / "_data"
THUMBS_DIR = ROOT / "assets" / "thumbs"
MASTER_CSV = DATA_DIR / "africanart_mdl_medata.csv"
SITE_CSV = DATA_DIR / "africanart_metadata.csv"
SOURCE_CSV = Path(
    "/Users/Birittany/Downloads/Data  Jackson State University African Art Collection - Data  Jackson State University African Art Collection (1).csv"
)
MAX_OBJECT_ID = 148
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff"}

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
    raw_parts = re.split(r"[;,]", value)
    parts = []
    for part in raw_parts:
        cleaned = re.sub(r"^(and|or)\s+", "", part.strip(), flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
        if cleaned:
            parts.append(cleaned)
    return "; ".join(parts)


COUNTRY_COORDS = {
    "mali": (17.5707, -3.9962),
    "democratic republic of the congo": (-2.8797, 23.6560),
    "democratic republic of the congo (uele region)": (3.0, 25.0),
    "democratic republic of the congo (kasai region)": (-6.0, 22.0),
    "democratic republic of the congo / angola": (-8.5, 18.5),
    "côte d’ivoire": (7.5400, -5.5471),
    "cote d’ivoire": (7.5400, -5.5471),
    "guinea": (9.9456, -9.6966),
    "gabon": (-0.8037, 11.6094),
    "liberia / côte d’ivoire": (6.5, -7.5),
    "liberia / cote d’ivoire": (6.5, -7.5),
    "nigeria": (9.0820, 8.6753),
}


def infer_searchable_date(value: str) -> str:
    text = (value or "").strip().lower()
    if not text or text == "?":
        return ""
    explicit_years = re.findall(r"(1[0-9]{3}|20[0-9]{2})", text)
    if explicit_years:
        return explicit_years[0]
    if "late 19th" in text and "early 20th" in text:
        return "1900"
    if "late 19th" in text:
        return "1890"
    if "early 20th" in text:
        return "1910"
    if "mid 20th" in text:
        return "1950"
    if "early–mid 20th" in text or "early-mid 20th" in text:
        return "1940"
    if "19th–20th" in text or "19th-20th" in text:
        return "1900"
    if "20th century" in text:
        return "1950"
    if "19th century" in text:
        return "1850"
    return ""


def infer_coordinates(*values: str):
    for value in values:
        normalized = (value or "").strip().lower()
        if normalized in COUNTRY_COORDS:
            lat, lon = COUNTRY_COORDS[normalized]
            return f"{lat:.4f}", f"{lon:.4f}"
    return "", ""


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
        if not row.get("Searchable date"):
            row["Searchable date"] = infer_searchable_date(date_text)
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

    if not row.get("latitude") or not row.get("longitude"):
        lat, lon = infer_coordinates(country, row.get("Geographic location"), row.get("place_of_creation"))
        row["latitude"] = row.get("latitude") or lat
        row["longitude"] = row.get("longitude") or lon

    return row


def sync_helper_fields(row):
    row["Object name"] = row.get("Object name", "") or row.get("Identifier", "")
    row["format"] = row.get("format", "") or mime_type(row.get("File name", ""))
    if row.get("Creator", "").strip().lower() == "unknown":
        row["Creator"] = ""
    if not row.get("Searchable date"):
        row["Searchable date"] = infer_searchable_date(row.get("Date", ""))
    if not row.get("latitude") or not row.get("longitude"):
        lat, lon = infer_coordinates(
            row.get("Geographic location", ""),
            row.get("place_of_creation", ""),
            row.get("place_of_use", ""),
        )
        row["latitude"] = row.get("latitude") or lat
        row["longitude"] = row.get("longitude") or lon
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
        "Creator": "",
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


def generate_thumbnails(rows):
    THUMBS_DIR.mkdir(parents=True, exist_ok=True)
    for row in rows:
        filename = (row.get("File name") or "").strip()
        if not filename:
            continue
        source_path = OBJECTS_DIR / filename
        if not source_path.exists():
            continue
        if source_path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        thumb_path = THUMBS_DIR / filename
        thumb_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "sips",
                "--resampleHeightWidthMax",
                "250",
                "--padToHeightWidth",
                "250",
                "250",
                str(source_path),
                "--out",
                str(thumb_path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def main():
    master_rows = load_or_seed_master()
    write_csv(MASTER_CSV, MASTER_HEADERS, master_rows)
    generate_thumbnails(master_rows)
    print(f"Wrote {len(master_rows)} master records to {MASTER_CSV}")


if __name__ == "__main__":
    main()
