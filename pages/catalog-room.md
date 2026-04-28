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
      <p class="page-intro">Review, refine, and save catalog records from a protected workspace designed for daily record editing.</p>
    </div>
  </div>
</section>

<section class="research-panel editor-shell">
  <div class="research-panel-header">
      <div>
        <p class="section-kicker">Edit Records</p>
        <h2 class="record-section-title">Record editing workspace</h2>
        <p class="section-lead">Select a record, confirm the image and identifying details, then move through the metadata sections from top to bottom before saving the revision.</p>
      </div>
      <div class="editor-page-actions">
        <button type="button" class="btn btn-outline-dark" id="editor-export-csv">Export all records as MDL CSV</button>
      </div>
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
        <p>The editor stays hidden from public navigation and only opens after you sign in with a staff account.</p>
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
            <button type="submit" class="btn btn-primary">Save draft</button>
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
            <p>Confirm the image and record identity first, then work from top to bottom through identification, cultural context, and descriptive notes. Use <strong>Save draft</strong> while you are still working, and use the final save button at the bottom of the form when the revision is ready.</p>
          </div>
        </div>

        <div id="editor-fields" class="editor-fields"></div>

        <div class="editor-save-bar">
          <div class="editor-save-copy">
            <span class="editor-field-label">Final Save</span>
            <p class="small-note mb-0">When you are finished reviewing the record, save your changes here.</p>
          </div>
          <div class="editor-save-actions">
            <input id="editor-commit-message" class="form-control" type="text" value="" placeholder="Optional note about this revision">
            <button type="button" class="btn btn-primary" id="editor-commit-csv">Save Record</button>
          </div>
        </div>
      </form>
    </div>
  </div>

  <div class="editor-settings-panel">
    <div class="editor-settings-header">
      <div>
        <p class="section-kicker">Site Settings</p>
        <h3 class="editor-settings-title">Site appearance</h3>
        <p class="small-note mb-0">Update collection-wide presentation details here, including colors, typography, and featured content shown across the site.</p>
      </div>
    </div>
    <div id="editor-settings-alert" class="access-alert d-none"></div>
    <form id="editor-settings-form" class="editor-settings-form">
      <label class="editor-field">
        <span class="editor-field-label">Primary color</span>
        <input id="settings-primary-color" class="form-control" type="text" placeholder="#14213d">
      </label>
      <label class="editor-field">
        <span class="editor-field-label">Secondary color</span>
        <input id="settings-secondary-color" class="form-control" type="text" placeholder="#243b63">
      </label>
      <label class="editor-field">
        <span class="editor-field-label">Text color</span>
        <input id="settings-text-color" class="form-control" type="text" placeholder="#111827">
      </label>
      <label class="editor-field">
        <span class="editor-field-label">Link color</span>
        <input id="settings-link-color" class="form-control" type="text" placeholder="#1f3a68">
      </label>
      <label class="editor-field">
        <span class="editor-field-label">Body font family</span>
        <input id="settings-body-font-family" class="form-control" type="text" placeholder="&quot;Source Sans 3&quot;, system-ui, sans-serif">
      </label>
      <label class="editor-field">
        <span class="editor-field-label">Heading font family</span>
        <input id="settings-heading-font-family" class="form-control" type="text" placeholder="&quot;Source Serif 4&quot;, Georgia, serif">
      </label>
      <label class="editor-field">
        <span class="editor-field-label">Featured object or image</span>
        <input id="settings-featured-image" class="form-control" type="text" placeholder="coll032 or /assets/img/banner.jpg">
      </label>
      <label class="editor-field">
        <span class="editor-field-label">Banner image position</span>
        <select id="settings-banner-position" class="form-control">
          <option value="center">Center</option>
          <option value="top">Top</option>
          <option value="bottom">Bottom</option>
          <option value="left">Left</option>
          <option value="right">Right</option>
        </select>
      </label>
      <div class="editor-settings-actions">
        <button type="button" class="btn btn-primary" id="settings-save-button">Save site settings</button>
      </div>
    </form>
  </div>
</section>
