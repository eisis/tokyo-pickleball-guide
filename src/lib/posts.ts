// 記事に関する共通の決まりごと。カテゴリの名前・説明・リンクの作り方はここだけで管理する。
// カテゴリを増やすときは POST_CATEGORIES に1行足し、content.config.ts の category にも追加する。
import { getCollection, getEntry, type CollectionEntry } from 'astro:content';

export type Post = CollectionEntry<'posts'>;

// 並び順もこの順番になる
export const POST_CATEGORIES = {
  review: { ja: 'コートレビュー', en: 'Court Reviews', desc: '実際に打ちに行ったコートの体験レビュー。景色、混み具合、レンタル、予約のコツまで。' },
  guide: { ja: 'はじめ方・ルール', en: 'Guides', desc: 'ルールや道具選び、上達のコツなど、これから始める人のためのガイド。' },
  roundup: { ja: 'まとめ', en: 'Roundups', desc: 'エリアやテーマごとに、コートを比べて選べるまとめ記事。' },
  news: { ja: 'ニュース', en: 'News', desc: '新しいコートのオープンなど、東京近郊のピックルボールの話題。' },
  event: { ja: '大会・イベント', en: 'Events', desc: '大会や体験会の情報と、参加してきたレポート。' },
} as const;
export type PostCategory = keyof typeof POST_CATEGORIES;

/** 公開中の記事を新しい順で返す */
export async function getPosts(): Promise<Post[]> {
  return (await getCollection('posts', (p) => !p.data.draft)).sort(
    (a, b) => b.data.publishedAt.getTime() - a.data.publishedAt.getTime()
  );
}

export const postUrl = (p: Post) => `/blog/${p.id}/`;
export const categoryUrl = (c: PostCategory) => `/blog/category/${c}/`;
export const tagUrl = (t: string) => `/blog/tag/${encodeURIComponent(t)}/`;
export const ymd = (d: Date) => d.toISOString().slice(0, 10).replaceAll('-', '.');

/** 本文の文字数から、読むのにかかる分数の目安（1分=500字） */
export const readingMinutes = (p: Post) =>
  Math.max(1, Math.round((p.body ?? '').replace(/!\[[^\]]*\]\([^)]*\)|[#*>\-`\s]/g, '').length / 500));

/** 一覧やSNSで使う画像：cover → 本文の最初の画像 → 紹介コートの画像 */
export async function coverOf(p: Post): Promise<{ src: string; alt: string } | null> {
  if (p.data.cover) return { src: p.data.cover, alt: p.data.coverAlt ?? p.data.title };
  const m = (p.body ?? '').match(/!\[([^\]]*)\]\(([^)\s]+)/);
  if (m) return { src: m[2], alt: m[1] || p.data.title };
  for (const id of p.data.courts) {
    const court = await getEntry('courts', id);
    if (court?.data.image) return { src: court.data.image, alt: court.data.name };
  }
  return null;
}

/** 本文の先頭の文（記事に description がない場合などに使う） */
export const searchText = (p: Post) =>
  [p.data.title, p.data.description, POST_CATEGORIES[p.data.category].ja, ...p.data.tags, (p.body ?? '').replace(/[#*>\[\]()!`\-]/g, ' ').slice(0, 1500)].join(' ');

/** 関連記事：同じカテゴリ・共通タグ・同じコートが多い順 */
export function relatedPosts(p: Post, all: Post[], n = 3): Post[] {
  const score = (o: Post) =>
    (o.data.category === p.data.category ? 2 : 0) +
    o.data.tags.filter((t) => p.data.tags.includes(t)).length +
    o.data.courts.filter((c) => p.data.courts.includes(c)).length * 2;
  return all
    .filter((o) => o.id !== p.id)
    .map((o) => ({ o, s: score(o) }))
    .sort((a, b) => b.s - a.s || b.o.data.publishedAt.getTime() - a.o.data.publishedAt.getTime())
    .slice(0, n)
    .map((x) => x.o);
}
