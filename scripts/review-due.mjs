// 見直しが必要なコートの一覧を出す（週次チェックが最初に実行する）。
// ・reviewBy（見直し日）が今日から7日以内、または過ぎているもの
// ・updatedAt（情報確認日）が60日より前のもの
// 使い方: node scripts/review-due.mjs        （JSONで出したいときは --json）
import { readdirSync, readFileSync } from 'node:fs';

const DIR = 'src/content/courts';
const today = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
const addDays = (d, n) => new Date(Date.parse(d) + n * 86400000).toISOString().slice(0, 10);
const soon = addDays(today, 7);
const old = addDays(today, -60);

const rows = [];
for (const f of readdirSync(DIR).filter((f) => f.endsWith('.md') && !f.startsWith('_'))) {
  const text = readFileSync(`${DIR}/${f}`, 'utf8');
  const get = (k) => text.match(new RegExp(`^${k}:\\s*(.+)$`, 'm'))?.[1]?.replace(/\s+#.*$/, '').trim();
  if (get('hidden') === 'true') continue;
  const reviewBy = get('reviewBy');
  const updatedAt = get('updatedAt');
  const reasons = [];
  if (reviewBy && reviewBy <= soon) reasons.push(reviewBy < today ? `見直し日を過ぎている（${reviewBy}）` : `見直し日が近い（${reviewBy}）`);
  if (updatedAt && updatedAt < old) reasons.push(`情報確認日が60日以上前（${updatedAt}）`);
  if (reasons.length) rows.push({ file: `${DIR}/${f}`, name: get('name'), reviewBy, updatedAt, reasons });
}

if (process.argv.includes('--json')) console.log(JSON.stringify(rows, null, 2));
else {
  console.log(`見直しが必要なコート：${rows.length}件（${today} 時点）`);
  for (const r of rows) console.log(`- ${r.name}（${r.file}）：${r.reasons.join('、')}`);
}
