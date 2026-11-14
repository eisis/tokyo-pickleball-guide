// /llms.txt：AI（ChatGPT・Perplexityなど）向けに、サイトの中身と主要ページを短くまとめたテキスト。
// 掲載データから毎回自動で作るので、コートや記事を増やせば自然に更新される
import type { APIRoute } from 'astro';
import { getCourts, PREFECTURES, ENVIRONMENTS, courtUrl, isPublic, hasRental } from '../lib/courts';
import { SPOTS, type SpotId } from '../lib/spots';
import { getPosts } from '../lib/posts';
import { SITE } from '../lib/site';

// 1施設1行：場所・屋内外と、確認できている料金・時間・アクセス・レンタル・確認日
const line = (c: Awaited<ReturnType<typeof getCourts>>[number]) => {
  const d = c.data;
  const facts = [
    `${PREFECTURES[d.prefecture].full}${d.area.ja}`,
    d.environment.map((e) => ENVIRONMENTS[e].ja).join('・'),
    d.price && `料金 ${d.price}`,
    d.hours && `時間 ${d.hours}`,
    d.access?.ja,
    hasRental(c) && '道具のレンタルあり',
    `情報確認日 ${d.updatedAt.toISOString().slice(0, 10)}`,
  ].filter(Boolean).join('／');
  return `- [${d.name}](${SITE.url}${courtUrl(c)}): ${facts}。${d.description.ja}`;
};

export const GET: APIRoute = async () => {
  const courts = await getCourts();
  const posts = await getPosts();
  const prefs = (Object.keys(PREFECTURES) as (keyof typeof PREFECTURES)[]).filter((p) => courts.some((c) => c.data.prefecture === p));

  const lines = [
    `# ${SITE.name}`,
    '',
    `> ${SITE.description} 掲載内容は各施設・自治体・主催者の公式情報で確認したものに限り、毎週見直しています。コートごとに情報確認日を載せています。`,
    '',
    '## エリア別のコート一覧',
    ...prefs.map((p) => `- [${PREFECTURES[p].ja}のピックルボールコート一覧](${SITE.url}/areas/${p}/)`),
    '',
    '## 駅・街から探す',
    ...(Object.keys(SPOTS) as SpotId[]).map((k) => `- [${SPOTS[k].ja}のピックルボールコート](${SITE.url}/spots/${k}/)`),
    '',
    '## コート（専用コート・ジムなど）',
    ...courts.filter((c) => !isPublic(c)).map(line),
    '',
    '## 自治体の体育館・スポーツセンター（ピックルボールの一般公開・個人参加・教室）',
    ...courts.filter(isPublic).map(line),
    '',
    '## イベント',
    `- [今週参加できる練習会・体験会](${SITE.url}/this-week/)`,
    `- [大会・練習会・体験会の一覧](${SITE.url}/events/)`,
    '',
    '## 記事',
    ...posts.map((p) => `- [${p.data.title}](${SITE.url}/blog/${p.id}/): ${p.data.description}`),
    '',
    '## 運営',
    `- 運営：${SITE.name}（問い合わせ info@pickleball-tokyo.com、Instagram / X @pickleballtokyo）`,
    `- [コート運営者の方へ（掲載・更新）](${SITE.url}/owners/)`,
    '',
  ];
  return new Response(lines.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
