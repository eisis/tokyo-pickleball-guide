// 新しいピックルボールコートの候補をニュースから探し、GitHubのIssueにまとめる。
// 自動でサイトに載せるのではなく「候補を知らせる」だけ。載せるかどうかは人が判断する。
import { readdirSync, readFileSync } from 'node:fs';

const QUERIES = [
  'ピックルボール コート オープン',
  'ピックルボール 開業',
  'ピックルボール 新設 東京',
  'ピックルボール 新設 神奈川',
  'ピックルボール 新設 千葉',
  'ピックルボール 新設 埼玉',
];
const AREA = /東京|都内|神奈川|横浜|川崎|相模原|藤沢|湘南|埼玉|さいたま|川口|所沢|越谷|川越|千葉|船橋|柏|浦安|幕張|松戸|市川|[一-龥]{1,3}区/;
const DAYS = 8; // 週1回実行なので、直近8日分を見る

// すでに掲載しているコート名（重複を除くため）
const known = readdirSync('src/content/courts')
  .filter((f) => f.endsWith('.md'))
  .map((f) => (readFileSync(`src/content/courts/${f}`, 'utf8').match(/^name:\s*(.+)$/m)?.[1] ?? '').trim().toLowerCase())
  .filter(Boolean);

const decode = (s) =>
  s.replace(/<!\[CDATA\[|\]\]>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'");

async function search(q) {
  const url = `https://news.google.com/rss/search?q=${encodeURIComponent(q)}+when:${DAYS}d&hl=ja&gl=JP&ceid=JP:ja`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`news ${res.status}`);
  const xml = await res.text();
  return [...xml.matchAll(/<item>([\s\S]*?)<\/item>/g)].map(([, it]) => ({
    title: decode(it.match(/<title>([\s\S]*?)<\/title>/)?.[1] ?? ''),
    link: decode(it.match(/<link>([\s\S]*?)<\/link>/)?.[1] ?? ''),
    date: it.match(/<pubDate>([\s\S]*?)<\/pubDate>/)?.[1] ?? '',
  }));
}

const seen = new Set();
const candidates = [];
for (const q of QUERIES) {
  try {
    for (const item of await search(q)) {
      const key = item.title.replace(/\s+-\s+[^-]+$/, ''); // 末尾の「- 媒体名」を除いて重複判定
      if (seen.has(key)) continue;
      seen.add(key);
      if (!/ピックルボール|pickleball/i.test(item.title)) continue;
      if (!AREA.test(item.title)) continue;
      const lower = item.title.toLowerCase();
      const already = known.find((n) => lower.includes(n));
      candidates.push({ ...item, already });
    }
  } catch (e) {
    console.error(`検索失敗: ${q}: ${e.message}`);
  }
}

const fresh = candidates.filter((c) => !c.already);
console.log(`候補 ${fresh.length} 件（掲載済みと思われるもの ${candidates.length - fresh.length} 件を除外）`);
for (const c of fresh) console.log(`- ${c.title}\n  ${c.link}`);

// GitHub Actions上ならIssueを作る（候補がなければ作らない）
const { GITHUB_TOKEN, GITHUB_REPOSITORY } = process.env;
if (GITHUB_TOKEN && GITHUB_REPOSITORY && fresh.length) {
  const today = new Date().toISOString().slice(0, 10);
  const body = [
    '直近1週間のニュースから、新しいコートの可能性がある記事を集めました。',
    '掲載する場合は `src/content/courts/` に新しいファイルを追加してください（書き方はREADME）。',
    '',
    ...fresh.map((c) => `- [ ] [${c.title}](${c.link})`),
  ].join('\n');
  const res = await fetch(`https://api.github.com/repos/${GITHUB_REPOSITORY}/issues`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${GITHUB_TOKEN}`, Accept: 'application/vnd.github+json' },
    body: JSON.stringify({ title: `新コート候補 ${today}（${fresh.length}件）`, body }),
  });
  console.log(res.ok ? 'Issueを作成しました' : `Issue作成に失敗: ${res.status} ${await res.text()}`);
}
