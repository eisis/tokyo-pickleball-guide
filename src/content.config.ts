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
    // ↓ 確認できたものだけ書く（書いていなければサイトには出ない）
    rental: z.object({
      status: z.enum(['free', 'paid', 'none']), // free=無料で借りられる / paid=有料で借りられる / none=借りられない
      note: z.string().optional(), // 何を借りられるか（例: パドル・ボール）
    }).optional(),
    reservation: z.array(z.enum(['online', 'phone', 'walkin'])).min(1).optional(), // 予約方法：online=ネット / phone=電話 / walkin=当日受付
    description: ja_en, // カードに出る短い紹介文
    image: z.string().optional(), // public/images/courts/ の画像。なければ🏓を表示
    imageSource: z.string().url().optional(), // 画像の取得元（自動取得したとき書き込まれる）
    officialUrl: z.string().url().optional(), // 施設の公式サイト（画像の自動取得に使う）
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
    category: z.enum(['review', 'guide', 'roundup', 'news', 'event']).default('news'), // 種類（src/lib/posts.ts の POST_CATEGORIES）
    tags: z.array(z.string()).default([]), // 自由なタグ（エリア名・テーマなど）。タグごとの一覧ページが自動で作られる
    cover: z.string().optional(), // 一覧やSNSで使う画像（なければ本文の最初の画像 → 紹介コートの画像の順で自動）
    coverAlt: z.string().optional(),
    featured: z.boolean().default(false),
    points: z.array(z.string()).max(4).default([]), // 記事の冒頭に出す「この記事のポイント」（3つがおすすめ）
    facts: z.array(z.object({ label: z.string(), value: z.string() })).default([]), // 冒頭に出す情報の表（コートレビューの料金・アクセスなど） // true にすると記事一覧の一番上に大きく出る
    author: z.string().default('Pickleball Tokyo 編集部'),
    courts: z.array(z.string()).default([]), // 記事で紹介するコートのファイル名（関連リンクを出す）
    draft: z.boolean().default(false), // trueの間は公開しない
  }),
});

export const collections = { courts, posts };
