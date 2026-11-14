// 駅・街の単位でコートをまとめるページ（/spots/<id>/）の一覧。
// Search Console で「地名 ピックルボール」の検索が多い場所から作る。中身（料金・時間など）はコートのファイルから自動で出す
export const SPOTS = {
  toyosu: {
    ja: '豊洲・有明',
    pref: 'tokyo',
    courts: ['picklr-toyosu', 'pickleball-park-toyosu', 'pacific-pickle-club'],
    lead: '豊洲・新豊洲・有明の湾岸エリアには、屋内の会員制クラブから水辺の屋外コートまで、タイプの違うピックルボールコートが集まっています。',
  },
} as const;
export type SpotId = keyof typeof SPOTS;
export const spotOf = (courtId: string) =>
  (Object.keys(SPOTS) as SpotId[]).find((s) => (SPOTS[s].courts as readonly string[]).includes(courtId));
