// イベント（大会・練習会・体験会など）の共通の決まりごと。表示名・並び順・日付の扱いはここだけで管理する。
// 種類を増やすときは EVENT_TYPES に1行足し、content.config.ts の type にも追加する。
import { getCollection, getEntry, type CollectionEntry } from 'astro:content';
import { PREFECTURES } from './courts';

export type Event = CollectionEntry<'events'>;
type Court = CollectionEntry<'courts'>;

export const EVENT_TYPES = {
  tournament: { ja: '大会', en: 'Tournament' },
  practice: { ja: '練習会', en: 'Open Play' },
  trial: { ja: '体験会', en: 'Trial' },
  lesson: { ja: 'レッスン', en: 'Lesson' },
  festival: { ja: 'イベント', en: 'Festival' },
} as const;

export const LEVELS = {
  beginner: { ja: '初心者向け', en: 'Beginners' },
  all: { ja: 'どなたでも', en: 'All levels' },
  intermediate: { ja: '中級以上', en: 'Intermediate+' },
  advanced: { ja: '上級', en: 'Advanced' },
} as const;

/** 初心者が参加しやすいか（絞り込みの「初心者OK」） */
export const beginnerOk = (e: Event) => e.data.level === 'beginner' || e.data.level === 'all';

/** 日付 → "2026-11-01"（YAMLの日付はUTCの0時で読まれるので、そのまま切り出せば日本の日付になる） */
export const iso = (d: Date) => d.toISOString().slice(0, 10);
/** 日本時間の今日 "2026-10-17" */
export const todayJst = () => new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);

const WEEK = ['日', '月', '火', '水', '木', '金', '土'];
/** "11/1（日）" */
export const md = (d: Date) => `${d.getUTCMonth() + 1}/${d.getUTCDate()}（${WEEK[d.getUTCDay()]}）`;

export const eventUrl = (e: Event) => `/events/${e.id}/`;

/** 今日以降の開催日（ビルド時点。サイト上ではスクリプトで毎回もう一度判定する） */
export const upcomingDates = (e: Event, today = todayJst()) => e.data.dates.map(iso).filter((d) => d >= today).sort();

export type Venue = { name: string; address?: string; prefecture?: keyof typeof PREFECTURES; area?: string; court?: Court };

/** 会場：コートを指定していればコートの情報、なければ venue の情報 */
export async function venueOf(e: Event): Promise<Venue> {
  if (e.data.court) {
    const court = await getEntry('courts', e.data.court);
    if (!court) throw new Error(`イベント ${e.id}: court「${e.data.court}」が見つかりません（コートのファイル名を確認してください）`);
    return { name: court.data.name, address: court.data.address, prefecture: court.data.prefecture, area: court.data.area.ja, court };
  }
  if (!e.data.venue) throw new Error(`イベント ${e.id}: court か venue のどちらかを書いてください`);
  return { ...e.data.venue, prefecture: e.data.prefecture };
}

/** 公開中で、まだ開催日が残っているイベントを「主催 → 次の開催日」順で返す */
export async function getUpcomingEvents(): Promise<Event[]> {
  const today = todayJst();
  return (await getCollection('events', (e) => !e.data.hidden))
    .filter((e) => upcomingDates(e, today).length > 0)
    .sort(
      (a, b) =>
        Number(b.data.organizer.self) - Number(a.data.organizer.self) ||
        upcomingDates(a, today)[0].localeCompare(upcomingDates(b, today)[0])
    );
}

/** 詳細ページ用：公開中のイベントすべて（終了したものもページは残し「終了しました」と出す） */
export const getAllEvents = () => getCollection('events', (e) => !e.data.hidden);
