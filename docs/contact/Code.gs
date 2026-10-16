// ============================================================
// お問い合わせ受付台帳（Google Apps Script）
// スプレッドシートの「拡張機能 > Apps Script」に貼り付けて使います。
// 下の SECRET を、Vercel の SHEET_WEBHOOK_SECRET と同じ文字列にしてください。
// ============================================================

const SECRET = 'ここに合言葉を入れる';
const SHEET_NAME = '受付台帳';
const HEADERS = ['受付番号', '受付日時', '種別', 'お名前', 'メール', '件名', '内容', '送信元ページ', 'ステータス', '担当メモ'];

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    if (body.secret !== SECRET) return json({ ok: false, error: 'forbidden' });

    const sheet = getSheet();
    const r = body.row;
    sheet.appendRow([r.id, r.receivedAt, r.type, r.name, r.email, r.subject, r.details, r.source, '未対応', '']);
    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: String(err) });
  }
}

function getSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow(HEADERS);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold').setBackground('#d8f0ef');
    // ステータス列をプルダウンに
    const rule = SpreadsheetApp.newDataValidation().requireValueInList(['未対応', '対応中', '完了', '対応不要'], true).build();
    sheet.getRange(2, 9, 1000, 1).setDataValidation(rule);
    sheet.setColumnWidth(7, 420);
  }
  return sheet;
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

// 動作確認用：Apps Script の画面でこの関数を選んで「実行」すると台帳にテスト行が入ります
function testAppend() {
  getSheet().appendRow(['PT-TEST', new Date().toLocaleString('ja-JP'), 'テスト', 'テスト太郎', 'test@example.com', '', '動作確認', '', '未対応', '']);
}
