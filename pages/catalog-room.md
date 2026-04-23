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
      <p class="page-intro">Review, refine, and save catalog records from a protected workspace that stays outside the public site navigation.</p>
    </div>
    <div class="page-aside-card">
      <h2 class="h5">Current behavior</h2>
      <p>This editor can save local drafts in the browser and save approved changes directly to the live Supabase catalog.</p>
      <p class="mb-0"><strong>Hidden access:</strong> this page is not linked in the public navigation and can also be opened with <kbd>Shift</kbd> + <kbd>E</kbd> after unlocking research access.</p>
    </div>
  </div>
</section>

<section class="research-panel editor-shell">
  <div class="research-panel-header">
      <div>
        <p class="section-kicker">Record Editing</p>
        <h2 class="record-section-title">Catalog editing workspace</h2>
        <p class="section-lead">Use the left panel to locate a record, review the image and record summary, and then move through the metadata sections in a consistent order before saving your revision.</p>
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
        Start with the title or object ID, then confirm image, place, and culture before editing longer interpretive fields.
      </div>
      <div id="editor-record-list" class="editor-record-list" aria-live="polite"></div>
    </aside>

    <div class="editor-main">
      <div id="editor-empty" class="editor-empty">
        <h3>Select a record to begin.</h3>
        <p>The editor stays hidden from public navigation and only works after the staff password has been accepted in this browser.</p>
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
            <button type="button" class="btn btn-outline-dark" id="editor-copy-json">Copy JSON</button>
            <button type="button" class="btn btn-outline-dark" id="editor-download-json">Download JSON</button>
            <button type="submit" class="btn btn-primary">Save draft</button>
          </div>
        </div>

        <div class="editor-status-row">
          <div id="editor-alert" class="access-alert d-none"></div>
          <div id="editor-last-saved" class="editor-last-saved"></div>
        </div>

        <div class="editor-github-panel">
          <div>
            <span class="editor-field-label">Staff sign-in</span>
            <p class="small-note mb-0">Sign in with an authorized staff account to save changes from this device. Local draft saving will still work without sign-in.</p>
          </div>
          <div class="editor-github-row">
            <input id="editor-staff-email" class="form-control" type="email" autocomplete="username" placeholder="Staff email">
            <input id="editor-staff-password" class="form-control" type="password" autocomplete="current-password" placeholder="Staff password">
            <button type="button" class="btn btn-outline-dark" id="editor-staff-login">Sign in</button>
            <button type="button" class="btn btn-outline-dark d-none" id="editor-staff-logout">Sign out</button>
          </div>
          <p id="editor-staff-status" class="small-note editor-staff-status mb-0">Staff sign-in is required before changes can be saved to the live catalog.</p>
        </div>

        <div class="editor-github-panel">
          <div>
            <span class="editor-field-label">Catalog save</span>
            <p class="small-note mb-0">Saving writes directly to the live Supabase catalog. Treat the message field as a short internal note describing what changed.</p>
          </div>
          <div class="editor-github-row">
            <input id="editor-commit-message" class="form-control" type="text" value="" placeholder="Example: revised title and culture/community">
            <button type="button" class="btn btn-primary" id="editor-commit-csv">Save to Catalog</button>
          </div>
        </div>

        <div class="editor-preview-row">
          <div class="editor-preview-card">
            <div class="record-image-shell">
              <img id="editor-preview-image" class="protected-image" alt="">
            </div>
          </div>
          <div class="editor-preview-note">
            <h4>Suggested workflow</h4>
            <p>Confirm the image and record identity first, then work from top to bottom through identification, cultural context, and interpretive notes. Save a browser draft while you are still researching; use <strong>Save to Catalog</strong> once the revision is ready.</p>
          </div>
        </div>

        <div id="editor-fields" class="editor-fields"></div>
      </form>
    </div>
  </div>
</section>
