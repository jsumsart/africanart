---
title: Site Settings
layout: page
permalink: /site-settings.html
custom-foot: js/catalog-editor-auth.html;js/site-settings-editor.html
search_exclude: true
---

<section class="page-hero page-hero-compact">
  <div class="page-hero-grid page-hero-grid-tight">
    <div>
      <p class="section-kicker">Staff Workspace</p>
      <h1 class="page-title">Site Settings</h1>
      <p class="page-intro">Update collection-wide presentation details from a separate protected workspace, away from the day-to-day record editing view.</p>
    </div>
  </div>
</section>

<section class="research-panel editor-shell">
  <div class="research-panel-header">
    <div>
      <p class="section-kicker">Catalog Publish</p>
      <h2 class="record-section-title">Import updated MDL CSV</h2>
      <p class="section-lead">Use this admin-only tool after student work in Google Sheets is complete. Upload the revised CSV, confirm the header structure, then publish it back to the master catalog file in GitHub.</p>
    </div>
  </div>

  <div class="editor-settings-panel editor-settings-panel-page">
    <div class="editor-settings-header">
      <div>
        <p class="section-kicker">CSV Import</p>
        <h3 class="editor-settings-title">Replace the master catalog file</h3>
        <p class="small-note mb-0">This tool is for final publishing only. Students should still work in Google Sheets, not in this import view.</p>
      </div>
    </div>
    <div id="csv-import-alert" class="access-alert d-none"></div>
    <div class="csv-import-grid">
      <label class="editor-field">
        <span class="editor-field-label">Updated MDL CSV</span>
        <input id="csv-import-file" class="form-control" type="file" accept=".csv,text/csv">
      </label>
      <label class="editor-field">
        <span class="editor-field-label">GitHub publish token</span>
        <input id="csv-import-token" class="form-control" type="password" placeholder="github_pat_...">
      </label>
      <label class="editor-field csv-import-wide">
        <span class="editor-field-label">Publish note</span>
        <input id="csv-import-message" class="form-control" type="text" placeholder="Update master catalog from Google Sheets review">
      </label>
    </div>
    <p class="small-note mb-3">The GitHub publish token is only for final admin import. It is stored in this browser for convenience and can be replaced at any time.</p>
    <div id="csv-import-summary" class="editor-sidebar-tip editor-workflow-tip">
      Choose a CSV export from Google Sheets to validate its headers and row count before publishing.
    </div>
    <div class="editor-settings-actions">
      <button type="button" class="btn btn-outline-dark" id="csv-import-validate">Validate CSV</button>
      <button type="button" class="btn btn-primary" id="csv-import-publish">Publish CSV to GitHub</button>
    </div>
  </div>
</section>

<section class="research-panel editor-shell">
  <div class="research-panel-header">
    <div>
      <p class="section-kicker">Presentation Settings</p>
      <h2 class="record-section-title">Site appearance</h2>
      <p class="section-lead">Use this page for collection-wide visual settings such as colors, typography, and featured content. Record editing remains in Catalog Room.</p>
    </div>
    <div class="editor-page-actions">
      <a class="btn btn-outline-dark" href="{{ '/catalog-room.html' | relative_url }}">Back to Catalog Room</a>
    </div>
  </div>

  <div class="editor-settings-panel editor-settings-panel-page">
    <div class="editor-settings-header">
      <div>
        <p class="section-kicker">Site Settings</p>
        <h3 class="editor-settings-title">Collection-wide display settings</h3>
        <p class="small-note mb-0">Use this page to review collection-wide display settings. Direct save can be reconnected separately from the Google Sheets catalog workflow.</p>
      </div>
    </div>
    <div id="editor-settings-alert" class="access-alert d-none"></div>
    <div id="editor-settings-last-saved" class="editor-last-saved mb-3"></div>
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
