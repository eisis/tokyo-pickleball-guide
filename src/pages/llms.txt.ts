// /llms.txt：AI（ChatGPT・Perplexityなど）向けに、サイトの中身と主要ページを短くまとめたテキスト。
// 掲載データから毎回自動で作るので、コートや記事を増やせば自然に更新される
import type { APIRoute } from 'astro';
import { getCourts, PREFECTURES, ENVIRONMENTS, courtUrl } from '../lib/courts';
import { getPosts } from '../lib/posts';
import { SITE } from '../lib/site';

export const GET: APIRoute = async () => {
  const courts = await getCourts();
  const posts = await getPosts();
  const prefs = (Object.keys(PREFECTURES) as (keyof typeof PREFECTURES)[]).filter((p) => courts.some((c) => c.data.prefecture === p));

  const lines = [
    `# ${SITE.name}`,
    '',
    `> ${SITE.description} 掲載内容は各施設の公式情報で確認したものに限り、コートごとに情報確認日を載せています。`,
    '',
    '## エリア別のコート一覧',
    ...prefs.map((p) => `- [${PREFECTURES[p].ja}のピックルボールコート一覧](${SITE.url}/areas/${p}/)`),
    '',
    '## コート',
    ...courts.map(
      (c) =>
        `- [${c.data.name}](${SITE.url}${courtUrl(c)}): ${PREFECTURES[c.data.prefecture].full}${c.data.area.ja}、${c.data.environment.map((e) => ENVIRONMENTS[e].ja).join('・')}。${c.data.description.ja}`
    ),
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
