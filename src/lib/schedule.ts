// 「いつ・どこで打てるか」の予定一覧。イベント（events）と、施設の定期開催の枠（コートの sessions）をひとつの並びにする。
// 今週ページ（/this-week/）とエリアページの「今週の開催」で同じものを使う（並べ方を変えるときはここだけ直す）
import { getUpcomingEvents, venueOf, upcomingDates, startTime, type Event, type Venue } from './events';
import { getCourts, sessionDates, type Court } from './courts';

export type ScheduleItem =
  | { kind: 'event'; e: Event; venue: Venue; date: string; pref: string; self: boolean; time: string }
  | { kind: 'session'; c: Court; s: Court['data']['sessions'][number]; date: string; pref: string; self: false; time: string };

/** 今日以降の予定を「日付 → Pickleball Tokyo 主催 → 開始時刻」の順で返す */
export async function getSchedule(): Promise<ScheduleItem[]> {
  const events = (
    await Promise.all(
      (await getUpcomingEvents()).map(async (e) => {
        const venue = await venueOf(e);
        return upcomingDates(e).map((date) => ({ kind: 'event' as const, e, venue, date, pref: venue.prefecture ?? '', self: e.data.organizer.self, time: startTime(e) || '99:99' }));
      })
    )
  ).flat();
  const sessions = (await getCourts()).flatMap((c) =>
    sessionDates(c).map((x) => ({ kind: 'session' as const, c, s: x.s, date: x.date, pref: c.data.prefecture, self: false as const, time: (x.s.time.match(/\d{1,2}:\d{2}/)?.[0] ?? '99:99').padStart(5, '0') }))
  );
  return [...events, ...sessions].sort((a, b) => a.date.localeCompare(b.date) || Number(b.self) - Number(a.self) || a.time.localeCompare(b.time));
}

/** 日本時間の今日から n 日分の日付 ["2026-11-14", ...] */
export const nextDays = (n = 7) => [...Array(n)].map((_, i) => new Date(Date.now() + 9 * 3600 * 1000 + i * 86400000).toISOString().slice(0, 10));
