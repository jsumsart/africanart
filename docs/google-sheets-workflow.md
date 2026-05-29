## Google Sheets Catalog Workflow

This project now treats Google Sheets as the collaborative editing workspace for students.

### Recommended workflow

1. Open `Catalog Room`.
2. Export `Export records for Google Sheets`.
3. Upload that CSV to Google Sheets.
4. Let students edit titles, identifiers, descriptions, and other metadata in the sheet.
5. Use the included image columns while visually matching digital records to physical objects.
6. Download the updated sheet as CSV when review is complete.
7. Open `Site Settings` and use the `Import updated MDL CSV` tool to publish that file back to the repository.
8. Let GitHub Pages rebuild from the updated master CSV.

### Image columns included in the export

- `Thumbnail URL`
  A direct link to the public thumbnail for the record.
- `Google Sheets Image`
  A ready-made `=IMAGE("...")` formula for Google Sheets.
- `Record URL`
  A direct link to the live public record page.

### Notes

- The exported CSV is intended for spreadsheet work, not as the final published site file.
- The repository CSV remains the published source that the public Jekyll site reads from.
- Students should not use the import tool. It is intended for final admin publishing only.
