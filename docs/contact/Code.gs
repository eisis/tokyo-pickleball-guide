// ============================================================
// お問い合わせ受付台帳（Google Apps Script）
// スプレッドシートの「拡張機能 > Apps Script」に貼り付けて使います。
// SECRET は Vercel の SHEET_WEBHOOK_SECRET と同じ文字列にしてください。
//
// ・種別ごとにタブを分けて、1項目1列で記録します（タブがなければ自動作成）
// ・フォームに項目が増えたら、右端に列が自動で追加されます
// ・列の並び替えや幅の変更は自由にしてOK（列名で照合するのでずれません）
// ・action: 'update' のときは、受付番号の行の列を書き換えます（掲載申請の承認・見送りで使用）
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
      if (body.action === 'update') return json(updateRow(body.sheet, body.id, body.cells || {}));
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

// 受付番号の行を探して、指定の列を書き換える（列がなければ右端に追加）
// 例：掲載申請が承認されたら「ステータス」を「完了」に、「公開日時」を記入
function updateRow(name, id, cells) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(name);
  if (!sheet) return { ok: false, error: 'sheet not found' };
  const headers = ensureHeaders(sheet, Object.keys(cells));
  const idCol = headers.indexOf('受付番号') + 1;
  if (idCol < 1 || sheet.getLastRow() < 2) return { ok: false, error: 'id column not found' };
  const ids = sheet.getRange(2, idCol, sheet.getLastRow() - 1, 1).getValues().map((r) => String(r[0]));
  const at = ids.indexOf(String(id));
  if (at === -1) return { ok: false, error: 'id not found' };
  Object.keys(cells).forEach((h) => sheet.getRange(at + 2, headers.indexOf(h) + 1).setValue(clean(cells[h])));
  return { ok: true };
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
