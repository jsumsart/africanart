function jsonResponse(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

function textResponse(text, mimeType) {
  return ContentService
    .createTextOutput(text)
    .setMimeType(mimeType || ContentService.MimeType.TEXT);
}

function getConfig_() {
  var props = PropertiesService.getScriptProperties();
  return {
    passwordHash: props.getProperty('EDITOR_PASSWORD_SHA256') || '',
    spreadsheetId: props.getProperty('SPREADSHEET_ID') || '',
    recordsSheetName: props.getProperty('RECORDS_SHEET_NAME') || 'catalog_records',
    settingsSheetName: props.getProperty('SETTINGS_SHEET_NAME') || 'site_settings'
  };
}

function getSpreadsheet_() {
  var config = getConfig_();
  if (!config.spreadsheetId) {
    throw new Error('SPREADSHEET_ID is not configured.');
  }
  return SpreadsheetApp.openById(config.spreadsheetId);
}

function getSheetOrThrow_(name) {
  var sheet = getSpreadsheet_().getSheetByName(name);
  if (!sheet) {
    throw new Error('Required sheet not found: ' + name);
  }
  return sheet;
}

function parseJsonBody_(e) {
  if (!e || !e.postData || !e.postData.contents) {
    return {};
  }
  return JSON.parse(e.postData.contents);
}

function verifyEditor_(body) {
  var expectedHash = getConfig_().passwordHash;
  if (!expectedHash) {
    throw new Error('EDITOR_PASSWORD_SHA256 is not configured.');
  }
  var providedHash = String(body.editor_session_hash || '');
  if (!providedHash || providedHash !== expectedHash) {
    throw new Error('Editor credentials were not recognized.');
  }
}

function getRecords_() {
  var sheet = getSheetOrThrow_(getConfig_().recordsSheetName);
  var values = sheet.getDataRange().getValues();
  if (!values.length) return [];
  var headers = values[0];
  var records = [];
  for (var i = 1; i < values.length; i++) {
    var row = values[i];
    var item = {};
    for (var j = 0; j < headers.length; j++) {
      item[String(headers[j])] = row[j] == null ? '' : String(row[j]);
    }
    records.push(item);
  }
  return records;
}

function getSettings_() {
  var sheet = getSheetOrThrow_(getConfig_().settingsSheetName);
  var values = sheet.getDataRange().getValues();
  var settings = {};
  for (var i = 1; i < values.length; i++) {
    var key = values[i][0];
    if (!key) continue;
    settings[String(key)] = values[i][1] == null ? '' : String(values[i][1]);
  }
  return settings;
}

function saveRecord_(record) {
  var config = getConfig_();
  var sheet = getSheetOrThrow_(config.recordsSheetName);
  var values = sheet.getDataRange().getValues();
  if (!values.length) {
    throw new Error('The records sheet does not contain a header row.');
  }
  var headers = values[0];
  var targetId = String(record['Object name'] || '').trim();
  if (!targetId) {
    throw new Error('Record payload must include Object name.');
  }

  var rowIndex = -1;
  for (var i = 1; i < values.length; i++) {
    if (String(values[i][0]) === targetId) {
      rowIndex = i + 1;
      break;
    }
  }

  var row = [];
  for (var j = 0; j < headers.length; j++) {
    var header = String(headers[j]);
    row.push(record.hasOwnProperty(header) ? record[header] : '');
  }

  if (rowIndex > -1) {
    sheet.getRange(rowIndex, 1, 1, row.length).setValues([row]);
  } else {
    sheet.appendRow(row);
  }
}

function saveSettings_(settings) {
  var config = getConfig_();
  var sheet = getSheetOrThrow_(config.settingsSheetName);
  var values = sheet.getDataRange().getValues();
  var indexByKey = {};
  for (var i = 1; i < values.length; i++) {
    var key = values[i][0];
    if (key) {
      indexByKey[String(key)] = i + 1;
    }
  }

  Object.keys(settings).forEach(function(key) {
    var value = settings[key];
    if (indexByKey.hasOwnProperty(key)) {
      sheet.getRange(indexByKey[key], 2).setValue(value);
    } else {
      sheet.appendRow([key, value]);
    }
  });
}

function csvEscape_(value) {
  var text = value == null ? '' : String(value);
  if (text.indexOf(',') > -1 || text.indexOf('"') > -1 || text.indexOf('\n') > -1) {
    return '"' + text.replace(/"/g, '""') + '"';
  }
  return text;
}

function buildCsv_() {
  var sheet = getSheetOrThrow_(getConfig_().recordsSheetName);
  var values = sheet.getDataRange().getValues();
  var rows = [];
  for (var i = 0; i < values.length; i++) {
    var row = values[i];
    var escaped = [];
    for (var j = 0; j < row.length; j++) {
      escaped.push(csvEscape_(row[j]));
    }
    rows.push(escaped.join(','));
  }
  return rows.join('\n') + '\n';
}

function doGet(e) {
  try {
    var action = (e && e.parameter && e.parameter.action) || 'bootstrap';
    if (action === 'bootstrap') {
      return jsonResponse({
        ok: true,
        records: getRecords_(),
        settings: getSettings_()
      });
    }
    if (action === 'export_csv') {
      return textResponse(buildCsv_(), ContentService.MimeType.CSV);
    }
    return jsonResponse({ ok: false, message: 'Unsupported action.' });
  } catch (error) {
    return jsonResponse({ ok: false, message: error.message || 'Request failed.' });
  }
}

function doPost(e) {
  try {
    var body = parseJsonBody_(e);
    verifyEditor_(body);

    var action = String(body.save_action_type || '').trim();
    if (action === 'record') {
      if (!body.record) throw new Error('A record payload is required.');
      saveRecord_(body.record);
      return jsonResponse({ ok: true, message: 'Record saved to Google Sheets.' });
    }

    if (action === 'settings') {
      if (!body.settings) throw new Error('A settings payload is required.');
      saveSettings_(body.settings);
      return jsonResponse({ ok: true, message: 'Site settings saved to Google Sheets.' });
    }

    throw new Error('Unsupported save action.');
  } catch (error) {
    return jsonResponse({ ok: false, message: error.message || 'Save failed.' });
  }
}
