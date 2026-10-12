// コンテンツの「型」を決めるファイル。
// コートや記事のファイルに書き忘れ・書き間違いがあると、公開前のビルドでエラーになって教えてくれる。
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const ja_en = z.object({ ja: z.string(), en: z.string() });

const courts = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: './src/content/courts' }), // _で始まるファイル（テンプレート）は除外
  schema: z.object({
    name: z.string(), // 施設名
    area: ja_en, // エリア表示（例: 新橋 / Shimbashi）
    prefecture: z.enum(['tokyo', 'kanagawa', 'saitama', 'chiba']),
    environment: z.array(z.enum(['indoor', 'outdoor'])).min(1),
    category: z.enum(['dedicated', 'fitness', 'public', 'circle']).default('dedicated'), // 専用コート / ジム・スクール / 公共施設 / サークル
    courts: z.number().optional(), // 面数
    address: z.string().optional(),
    access: ja_en.optional(), // 最寄り駅など
    hours: z.string().optional(), // 営業時間
    price: z.string().optional(), // 料金の目安
    description: ja_en, // カードに出る短い紹介文
    image: z.string().optional(), // public/images/courts/ の画像。なければ🏓を表示
    booking: z.object({
      url: z.string().url(),
      label: z.enum(['book', 'info']).default('book'), // book=予約する / info=詳細を見る
    }),
    availabilityUrl: z.string().url().optional(), // 空き状況ページ（あれば）
    location: z.object({ lat: z.number(), lng: z.number() }).optional(), // 地図のピン位置（なければ地図に出ない）
    mapQuery: z.string(), // Googleマップ検索語
    openedAt: z.coerce.date().optional(),
    updatedAt: z.coerce.date(), // 情報を最後に確認した日
    sources: z.array(z.string().url()).default([]), // 情報源
    hidden: z.boolean().default(false), // trueにするとサイトに出さない
  }),
});

const posts = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedAt: z.coerce.date(),
    updatedAt: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    courts: z.array(z.string()).default([]), // 記事で紹介するコートのファイル名（関連リンクを出す）
    draft: z.boolean().default(false), // trueの間は公開しない
  }),
});

export const collections = { courts, posts };
