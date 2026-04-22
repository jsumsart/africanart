---
title: Catalog Room
layout: page
permalink: /catalog-room.html
custom-foot: js/catalog-editor.html
search_exclude: true
---

<section class="page-hero page-hero-compact">
  <div class="page-hero-grid page-hero-grid-tight">
    <div>
      <p class="section-kicker">Staff Workspace</p>
      <h1 class="page-title">Catalog Room</h1>
      <p class="page-intro">Review, refine, and stage record changes from a protected workspace that stays outside the public site navigation.</p>
    </div>
    <div class="page-aside-card">
      <h2 class="h5">Current behavior</h2>
      <p>This editor saves drafts in this browser only. Use the export tools to hand off or preserve changes before they are written back to the master catalog.</p>
      <p class="mb-0"><strong>Hidden access:</strong> this page is not linked in the public navigation and can also be opened with <kbd>Shift</kbd> + <kbd>E</kbd> after unlocking research access.</p>
    </div>
  </div>
</section>

<section class="research-panel editor-shell">
  <div class="research-panel-header">
    <div>
      <p class="section-kicker">Record Editing</p>
      <h2 class="record-section-title">Protected draft editor</h2>
      <p class="section-lead">Use the left panel to locate a record, then revise the catalog fields on the right. Drafts are stored locally in your browser until you export them.</p>
    </div>
  </div>

  <div class="editor-grid">
    <aside class="editor-sidebar">
      <label class="form-label" for="editor-search">Find a record</label>
      <input id="editor-search" class="form-control editor-search" type="search" placeholder="Search by object id, title, community, or place">
      <div class="editor-sidebar-meta">
        <span id="editor-count">0 records</span>
        <span id="editor-draft-count">0 drafts</span>
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

        <div class="editor-preview-row">
          <div class="editor-preview-card">
            <div class="record-image-shell">
              <img id="editor-preview-image" class="protected-image" alt="">
            </div>
          </div>
          <div class="editor-preview-note">
            <h4>Draft handling</h4>
            <p>Drafts remain in this browser under the current access session. They do not publish to the website until we intentionally write them back to the master CSV.</p>
          </div>
        </div>

        <div id="editor-fields" class="editor-fields"></div>
      </form>
    </div>
  </div>
</section>
