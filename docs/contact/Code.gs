// ============================================================
// お問い合わせ受付台帳（Google Apps Script）
// スプレッドシートの「拡張機能 > Apps Script」に貼り付けて使います。
// SECRET は Vercel の SHEET_WEBHOOK_SECRET と同じ文字列にしてください。
//
// ・種別ごとにタブを分けて、1項目1列で記録します（タブがなければ自動作成）
// ・フォームに項目が増えたら、右端に列が自動で追加されます
// ・列の並び替えや幅の変更は自由にしてOK（列名で照合するのでずれません）
// ============================================================

const SECRET = 'ここに合言葉を入れる';
const STATUS_HEADER = 'ステータス';
const STATUS_OPTIONS = ['未対応', '対応中', '完了', '対応不要'];

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    if (body.secret !== SECRET) return json({ ok: false, error: 'forbidden' });

    const lock = LockService.getScriptLock();
    lock.waitLock(10000);
    try {
      const sheet = getSheet(body.sheet, body.headers);
      const headers = ensureHeaders(sheet, body.headers);
      const row = headers.map((h) => clean(body.row[h]));
      sheet.appendRow(row);
    } finally {
      lock.releaseLock();
    }
    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: String(err) });
  }
}

// タブを取得（なければ作る）
function getSheet(name, headers) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.appendRow(headers);
    sheet.setFrozenRows(1);
    styleHeader(sheet, 1, headers.length);
    const col = headers.indexOf(STATUS_HEADER) + 1;
    if (col > 0) {
      const rule = SpreadsheetApp.newDataValidation().requireValueInList(STATUS_OPTIONS, true).build();
      sheet.getRange(2, col, 2000, 1).setDataValidation(rule);
    }
  }
  return sheet;
}

// 1行目の列名を読み、足りない列を右端に追加して、最新の列名一覧を返す
function ensureHeaders(sheet, wanted) {
  const last = Math.max(sheet.getLastColumn(), 1);
  const headers = sheet.getRange(1, 1, 1, last).getValues()[0].map(String);
  wanted.forEach((h) => {
    if (headers.indexOf(h) === -1) {
      headers.push(h);
      sheet.getRange(1, headers.length).setValue(h);
      styleHeader(sheet, headers.length, 1);
    }
  });
  return headers;
}

function styleHeader(sheet, col, n) {
  sheet.getRange(1, col, 1, n).setFontWeight('bold').setBackground('#d8f0ef');
}

// 数式として解釈されないように・電話番号の先頭0が消えないようにする
function clean(v) {
  if (v === undefined || v === null) return '';
  const s = String(v);
  return /^[=+\-@]/.test(s) || /^0\d/.test(s) ? "'" + s : s;
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
