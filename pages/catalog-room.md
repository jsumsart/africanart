---
title: Catalog Room
layout: page
permalink: /catalog-room.html
custom-foot: js/catalog-editor-auth.html;js/catalog-editor.html
search_exclude: true
---

<section class="page-hero page-hero-compact">
  <div class="page-hero-grid page-hero-grid-tight">
    <div>
      <p class="section-kicker">Staff Workspace</p>
      <h1 class="page-title">Catalog Room</h1>
      <p class="page-intro">Review catalog records, confirm visual matches, and prepare spreadsheet-ready exports for collaborative work in Google Sheets.</p>
    </div>
  </div>
</section>

<section class="research-panel editor-shell">
  <div class="research-panel-header">
      <div>
        <p class="section-kicker">Edit Records</p>
        <h2 class="record-section-title">Catalog review workspace</h2>
        <p class="section-lead">Use this page to review records, confirm object images, and export the working catalog for student editing in Google Sheets. The sheet should remain the day-to-day editing workspace.</p>
      </div>
      <div class="editor-page-actions">
        <a class="btn btn-outline-dark" href="{{ '/site-settings.html' | relative_url }}">Site settings</a>
        <button type="button" class="btn btn-outline-dark" id="editor-export-csv">Export records for Google Sheets</button>
      </div>
    </div>

  <div class="editor-sidebar-tip editor-workflow-tip">
    Suggested workflow: export the catalog from this page, let students work in Google Sheets with the image columns included, then download that sheet as CSV for final upload back into the master catalog.
  </div>

  <div class="editor-grid">
    <aside class="editor-sidebar">
      <label class="form-label" for="editor-search">Find a record</label>
      <input id="editor-search" class="form-control editor-search" type="search" placeholder="Search by object ID, title, culture, or place">
      <div class="editor-sidebar-meta">
        <span id="editor-count">0 records</span>
        <span id="editor-draft-count">0 drafts</span>
      </div>
      <div class="editor-sidebar-tip">
        Start with the title or object ID, then confirm image, place, and culture before editing longer descriptive fields.
      </div>
      <div id="editor-record-list" class="editor-record-list" aria-live="polite"></div>
    </aside>

    <div class="editor-main">
      <div id="editor-empty" class="editor-empty">
        <h3>Select a record to begin.</h3>
        <p>Open a record here when you want to verify titles, identifiers, and image matches before the spreadsheet is revised.</p>
      </div>

      <form id="editor-form" class="editor-form d-none">
        <div class="editor-form-header">
          <div>
            <p class="section-kicker">Active Record</p>
            <h3 id="editor-record-heading" class="editor-record-heading"></h3>
            <p id="editor-record-subtitle" class="editor-record-subtitle"></p>
          </div>
          <div class="editor-form-actions">
            <button type="button" class="btn btn-outline-dark" id="editor-reset">Reset draft</button>
            <button type="submit" class="btn btn-primary">Save browser draft</button>
          </div>
        </div>

        <div class="editor-status-row">
          <div id="editor-alert" class="access-alert d-none"></div>
          <div id="editor-last-saved" class="editor-last-saved"></div>
        </div>

        <div class="editor-preview-row">
          <div class="editor-preview-card">
            <div class="record-image-shell">
              <img id="editor-preview-image" class="protected-image editor-preview-image" alt="">
            </div>
          </div>
          <div class="editor-preview-note">
            <h4>Suggested workflow</h4>
            <p>Confirm the image and record identity first, then review identification, cultural context, and descriptive notes from top to bottom. Use <strong>Save browser draft</strong> only for temporary local notes while you compare the record against the Google Sheet.</p>
          </div>
        </div>

        <div id="editor-fields" class="editor-fields"></div>

        <div class="editor-save-bar">
          <div class="editor-save-copy">
            <span class="editor-field-label">Catalog Save</span>
            <p class="small-note mb-0">If a live save connection is configured, you can still save directly from this page. Otherwise, treat this area as a review aid and use the spreadsheet export as the primary working file.</p>
          </div>
          <div class="editor-save-actions">
            <input id="editor-commit-message" class="form-control" type="text" value="" placeholder="Optional note about this revision">
            <button type="button" class="btn btn-primary" id="editor-commit-csv">Save Record</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</section>
