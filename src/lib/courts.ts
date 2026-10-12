// コートに関する共通の決まりごと。表示名・並び順・リンクの作り方はここだけで管理する。
// 都道府県を増やすときは PREFECTURES に1行足し、content.config.ts の prefecture にも追加する。
import { getCollection, type CollectionEntry } from 'astro:content';

export type Court = CollectionEntry<'courts'>;
export type Environment = 'indoor' | 'outdoor';

// 並び順もこの順番になる
export const PREFECTURES = {
  tokyo: { ja: '東京', full: '東京都', en: 'Tokyo' },
  kanagawa: { ja: '神奈川', full: '神奈川県', en: 'Kanagawa' },
  saitama: { ja: '埼玉', full: '埼玉県', en: 'Saitama' },
  chiba: { ja: '千葉', full: '千葉県', en: 'Chiba' },
} as const;

// 施設の種類（専用コート以外はカードに小さく表示）
export const CATEGORIES = {
  dedicated: { ja: '専用コート', en: 'Dedicated' },
  fitness: { ja: 'ジム・スクール', en: 'Gym / School' },
  public: { ja: '公共施設', en: 'Public' },
  circle: { ja: 'サークル', en: 'Club' },
} as const;

export const ENVIRONMENTS = {
  indoor: { ja: '屋内', en: 'Indoor' },
  outdoor: { ja: '屋外', en: 'Outdoor' },
} as const;

/** 公開中のコートを、都道府県順→名前順で返す */
export async function getCourts(): Promise<Court[]> {
  const order = Object.keys(PREFECTURES);
  return (await getCollection('courts', (c) => !c.data.hidden)).sort(
    (a, b) =>
      order.indexOf(a.data.prefecture) - order.indexOf(b.data.prefecture) ||
      a.data.name.localeCompare(b.data.name, 'ja')
  );
}

export const courtUrl = (court: Court) => `/courts/${court.id}/`;
export const mapUrl = (court: Court) => `https://maps.google.com/?q=${encodeURIComponent(court.data.mapQuery)}`;

export const bookingLabel = (court: Court) =>
  court.data.booking.label === 'info' ? { ja: '詳細を見る →', en: 'Learn More →' } : { ja: '予約する →', en: 'Book Now →' };

/** 開業から半年以内なら NEW */
export const isNew = (court: Court) =>
  !!court.data.openedAt && Date.now() - court.data.openedAt.getTime() < 1000 * 60 * 60 * 24 * 180;

/** 屋内・屋外・両方 の区分（地図のピンの色分けに使う） */
export const envKind = (court: Court): 'indoor' | 'outdoor' | 'both' =>
  court.data.environment.length > 1 ? 'both' : court.data.environment[0];
