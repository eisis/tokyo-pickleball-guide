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
      status: z.enum(['free', 'paid', 'available', 'none']), // free=無料 / paid=有料 / available=借りられる（料金は不明） / none=借りられない
      note: z.string().optional(), // 何を借りられるか（例: パドル・ボール）
    }).optional(),
    reservation: z.array(z.enum(['online', 'line', 'phone', 'walkin'])).min(1).optional(), // 予約方法：online=ネット / line=LINE / phone=電話 / walkin=当日受付
    description: ja_en, // カードに出る短い紹介文
    image: z.string().optional(), // public/images/courts/ の画像。なければ🏓を表示
    imageSource: z.string().url().optional(), // 画像の取得元（自動取得したとき書き込まれる）
    officialUrl: z.string().url().optional(), // 施設の公式サイト（画像の自動取得に使う）
    imageUrl: z.string().url().optional(), // コートが写っている写真のURL（あればシェア用画像より優先して取得）
    booking: z.object({
      url: z.string().url(),
      label: z.enum(['book', 'info']).default('book'), // book=予約する / info=詳細を見る
    }),
    bookingSystem: z.string().optional(), // 社内用メモ：予約に使っているシステム（例: RESERVA / STORES予約）。サイトには出さない
    availabilityUrl: z.string().url().optional(), // 空き状況ページ（あれば）
    location: z.object({ lat: z.number(), lng: z.number() }).optional(), // 地図のピン位置（なければ地図に出ない）
    mapQuery: z.string(), // Googleマップ検索語
    openedAt: z.coerce.date().optional(),
    closesAt: z.coerce.date().optional(), // 期間限定コートの営業最終日。この日が過ぎると、毎朝の再ビルドでサイトから自動で消える
    updatedAt: z.coerce.date(), // 情報を最後に確認した日
    sources: z.array(z.string().url()).default([]), // 情報源
    hidden: z.boolean().default(false), // trueにするとサイトに出さない
    ownerVerified: z.boolean().default(false), // 施設の運営者本人が掲載・更新した情報（「運営者掲載」マークが付く）
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
    coverFit: z.enum(['cover', 'contain']).default('cover'), // contain = 文字入りの画像など、切り取らずに全体を見せる
    featured: z.boolean().default(false),
    points: z.array(z.string()).max(4).default([]), // 記事の冒頭に出す「この記事のポイント」（3つがおすすめ）
    facts: z.array(z.object({ label: z.string(), value: z.string() })).default([]), // 冒頭に出す情報の表（コートレビューの料金・アクセスなど） // true にすると記事一覧の一番上に大きく出る
    author: z.string().default('Pickleball Tokyo 編集部'),
    courts: z.array(z.string()).default([]), // 記事で紹介するコートのファイル名（関連リンクを出す）
    draft: z.boolean().default(false), // trueの間は公開しない
  }),
});

// イベント（大会・練習会・体験会など）。1イベント＝1ファイル。書き方は src/content/events/_template.md
// 日付がすべて過ぎたイベントは、サイト上で自動的に「終了」扱いになり一覧から消える
const events = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: './src/content/events' }),
  schema: z.object({
    title: z.string(),
    type: z.enum(['tournament', 'practice', 'trial', 'lesson', 'festival']), // 大会 / 練習会・オープンプレー / 体験会 / レッスン / フェス・複合イベント
    dates: z.array(z.coerce.date()).min(1), // 開催日（複数日・定期開催はすべて並べる）
    time: z.string().optional(), // 例: "11:00〜15:00"
    schedule: z.string().optional(), // 定期開催のとき、一覧に出す言い方（例: "毎週火曜 19:00〜21:00"）。dates には開催日を並べる
    court: z.string().optional(), // 掲載中コートで開催するときはコートのファイル名（会場情報はコートから自動で入る）
    venue: z.object({ // 掲載していない会場のとき
      name: z.string(),
      address: z.string().optional(),
      location: z.object({ lat: z.number(), lng: z.number() }).optional(),
    }).optional(),
    prefecture: z.enum(['tokyo', 'kanagawa', 'saitama', 'chiba']).optional(), // court を書いたときは不要
    level: z.enum(['beginner', 'all', 'intermediate', 'advanced']).optional(), // 初心者向け / どなたでも / 中級以上 / 上級（主催者が書いていなければ省く）
    price: z.string().optional(), // 例: "無料" "1ペア 10,000円"
    entry: z.object({
      required: z.boolean().default(true), // false=予約不要・当日参加OK
      deadline: z.coerce.date().optional(), // 申込締切
      url: z.string().url().optional(), // 申込ページ（なければ url を使う）
      note: z.string().optional(),
    }).default({ required: true }),
    summary: z.string(), // 一覧に出る1〜2文の紹介
    url: z.string().url().optional(), // 主催者の公式ページ（詳細はこちらへ送る）
    organizer: z.object({
      id: z.string().optional(), // 主催者のファイル名（src/content/organizers/）。書くと主催者ページにまとまる
      name: z.string(),
      self: z.boolean().default(false), // true = Pickleball Tokyo 主催（一覧の先頭に目立たせ、申込をサイト内で受ける）
    }),
    organizerPosted: z.boolean().default(false), // 主催者本人が掲載フォームから載せたイベント（「主催者掲載」マークが付く）
    image: z.string().optional(),
    sources: z.array(z.string().url()).default([]),
    updatedAt: z.coerce.date(), // 情報を確認した日
    hidden: z.boolean().default(false),
  }),
});

// 主催者（サークル・施設・大会運営など）。1主催者＝1ファイル。イベント掲載フォームから自動で作られる
// trusted: true の主催者は、次回から同じメールアドレスの申し込みが、そのアドレスに届くボタンを押すだけで即時公開される
const organizers = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: './src/content/organizers' }),
  schema: z.object({
    name: z.string(),
    url: z.string().url().optional(), // 主催者のサイト・SNS
    description: z.string().optional(), // 主催者ページに出る紹介文
    trusted: z.boolean().default(false),
    emailKeys: z.array(z.string()).default([]), // 申込メールアドレスの照合用ハッシュ（サイトには出さない）
    self: z.boolean().default(false), // Pickleball Tokyo 自身
    since: z.coerce.date().optional(),
    hidden: z.boolean().default(false),
  }),
});

export const collections = { courts, posts, events, organizers };
