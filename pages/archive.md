---
title: Access Archive
layout: page
permalink: /archive.html
custom-foot: js/archive-list.html
---

{%- assign archive_items = site.data[site.metadata] | where_exp: 'item', 'item["Object name"] != nil' -%}

<section class="page-hero page-hero-compact">
  <div class="page-hero-grid page-hero-grid-tight">
    <div>
      <p class="section-kicker">Public Archive</p>
      <h1 class="page-title">Access Archive</h1>
      <p class="page-intro">This public archive lists the collection’s current records without opening the protected image-bearing portal. Use it to review identifiers, titles, cultures or communities, places, and dates.</p>
    </div>
  </div>
</section>

<section class="research-panel archive-shell">
  <div class="research-panel-header">
    <div>
      <p class="section-kicker">Collection List</p>
      <h2 class="record-section-title">Archive records</h2>
      <p class="section-lead">The archive is intended as a public-facing point of entry into the collection. Full portal tools and protected images remain available only after password access is opened.</p>
    </div>
  </div>

  <div class="archive-toolbar">
    <label class="editor-field archive-search-field" for="archive-search">
      <span class="editor-field-label">Search the public archive</span>
      <input id="archive-search" class="form-control" type="search" placeholder="Search by identifier, title, culture, place, or date">
    </label>
    <div class="archive-count" id="archive-count">{{ archive_items | size }} records</div>
  </div>

  <div class="archive-list" id="archive-list">
    {% for item in archive_items %}
    <article class="archive-record" data-archive-record data-search="{{ item.Identifier }} {{ item.Title }} {{ item.culture_community }} {{ item['Geographic location'] }} {{ item.Date }}">
      <div class="archive-record-main">
        <p class="archive-record-id">{{ item.Identifier | default: item["Object name"] }}</p>
        <h3 class="archive-record-title">{{ item.Title | default: item["Object name"] }}</h3>
        <p class="archive-record-meta">
          {% if item.culture_community %}<span>{{ item.culture_community }}</span>{% endif %}
          {% if item.culture_community and item["Geographic location"] %}<span>•</span>{% endif %}
          {% if item["Geographic location"] %}<span>{{ item["Geographic location"] }}</span>{% endif %}
          {% if item.Date %}<span>•</span><span>{{ item.Date }}</span>{% endif %}
        </p>
      </div>
      <div class="archive-record-actions d-none" data-home-unlocked>
        <a class="btn btn-outline-dark btn-sm" href="{{ '/item.html?id=' | relative_url }}{{ item['Object name'] }}">Open full record</a>
      </div>
    </article>
    {% endfor %}
  </div>

  <div class="archive-empty d-none" id="archive-empty">
    No archive records matched that search. Try a broader title, place, or identifier term.
  </div>
</section>
