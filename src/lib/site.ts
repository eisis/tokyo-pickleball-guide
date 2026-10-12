// サイト名・キャッチコピーなど、サイト全体の文言はここだけで管理する
export const SITE = {
  name: 'Pickleball Tokyo',
  url: 'https://www.pickleball-tokyo.com',
  // トップの見出しの下の文
  lead: {
    ja: '東京近郊のピックルボールコートを、地図とエリア別にまとめました。<br>屋内・屋外を比べて、そのまま予約できます。',
    en: 'Pickleball courts in and around Tokyo, on one map.<br>Compare indoor and outdoor courts and book directly.',
  },
  // 検索結果に出る説明文
  description:
    '東京近郊（東京・神奈川・千葉・埼玉）のピックルボールコートまとめ。地図とエリア別一覧で屋内・屋外コートを比較して、そのまま予約できます。',
} as const;
