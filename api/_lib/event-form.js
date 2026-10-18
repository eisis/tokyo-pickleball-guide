// ============================================================
// イベント掲載フォームの定義（主催者が自分でイベントを載せるためのフォーム）
// ・画面（src/pages/events/submit.astro）も受付API（api/event-submit.js）もこの定義を使う
// ・選択肢の v はイベントのファイル（content.config.ts の events）の値と同じ
// ・開催日（dates）は画面側で「くり返し」から組み立てて配列で送る（ここでは上限だけ決める）
// ============================================================

export const EVENT_TYPE_OPTIONS = [
  { v: 'practice', label: '練習会・オープンプレー' },
  { v: 'trial', label: '体験会' },
  { v: 'lesson', label: 'レッスン・クリニック' },
  { v: 'tournament', label: '大会' },
  { v: 'festival', label: 'フェス・複合イベント' },
];

export const LEVEL_OPTIONS = [
  { v: 'beginner', label: '初心者向け' },
  { v: 'all', label: 'どなたでも' },
  { v: 'intermediate', label: '中級以上' },
  { v: 'advanced', label: '上級' },
];

export const ENTRY_OPTIONS = [
  { v: 'required', label: '事前申込が必要' },
  { v: 'walkin', label: '予約不要（当日参加OK）' },
];

export const PREFECTURE_OPTIONS = [
  { v: 'tokyo', label: '東京都' },
  { v: 'kanagawa', label: '神奈川県' },
  { v: 'chiba', label: '千葉県' },
  { v: 'saitama', label: '埼玉県' },
];

// 申請者の立場。主催者本人か代理なら、承認後は「承認済みの主催者」として次回から即時公開になる
export const ROLE_OPTIONS = [
  { v: 'organizer', label: '主催者本人' },
  { v: 'staff', label: '主催団体・施設のスタッフ' },
  { v: 'info', label: '参加者・情報提供' },
];
export const ORGANIZER_ROLES = ['organizer', 'staff'];

export const DATE_LIMIT = { max: 24, daysAhead: 365 }; // 1回の申請で送れる開催日の数・何日先まで

export const SECTIONS = [
  {
    id: 'basic',
    title: 'イベントの内容',
    fields: [
      { name: 'title', label: 'イベント名', type: 'text', required: true, maxLength: 60, placeholder: '例：初心者歓迎オープンプレー（豊洲）' },
      { name: 'type', label: '種類', type: 'radio', required: true, options: EVENT_TYPE_OPTIONS },
      { name: 'level', label: '対象レベル', type: 'radio', required: true, options: LEVEL_OPTIONS, help: '迷ったら「どなたでも」。初心者向け・どなたでもは「初心者OK」の絞り込みに出ます。' },
      { name: 'summary', label: 'ひとこと紹介', type: 'textarea', required: true, maxLength: 120, rows: 3, placeholder: '例：ラリーができれば参加OK。集まった人でゲームを回します。パドルの貸し出しあり。', help: '一覧に出る1〜2文です。誰向けで、何ができるかを書くと選ばれやすくなります。' },
      { name: 'detail', label: '詳しい説明', type: 'textarea', required: false, maxLength: 1000, rows: 5, placeholder: '当日の流れ、持ち物、服装など', help: 'イベントのページに載ります（なくても大丈夫です）。' },
    ],
  },
  {
    id: 'when',
    title: '日時',
    lead: '定期開催は「くり返し」で日付をまとめて入れられます。',
    fields: [
      { name: 'dates', label: '開催日', type: 'dates', required: true },
      { name: 'timeStart', label: '開始時刻', type: 'time', required: true },
      { name: 'timeEnd', label: '終了時刻', type: 'time', required: false },
    ],
  },
  {
    id: 'where',
    title: '会場',
    fields: [
      { name: 'court', label: '会場', type: 'court', required: true, help: '掲載中のコートなら選ぶだけで、住所や地図が自動で入ります。' },
      { name: 'venueName', label: '会場名', type: 'text', required: true, maxLength: 60, showIf: { court: ['other'] } },
      { name: 'venuePref', label: '都道府県', type: 'select', required: true, options: PREFECTURE_OPTIONS, showIf: { court: ['other'] } },
      { name: 'venueAddress', label: '住所', type: 'text', required: true, maxLength: 120, showIf: { court: ['other'] }, autocomplete: 'street-address' },
    ],
  },
  {
    id: 'entry',
    title: '参加費・申込',
    fields: [
      { name: 'price', label: '参加費', type: 'text', required: true, maxLength: 40, placeholder: '例：1人 2,000円 ／ 無料' },
      { name: 'entry', label: '申込', type: 'radio', required: true, options: ENTRY_OPTIONS },
      { name: 'entryUrl', label: '申込ページのURL', type: 'url', required: true, maxLength: 300, placeholder: 'https://', showIf: { entry: ['required'] }, help: 'LINEのオープンチャット、Googleフォーム、予約サイトなど、参加者が申し込むページ。' },
      { name: 'deadline', label: '申込締切', type: 'date', required: false, showIf: { entry: ['required'] } },
      { name: 'url', label: '詳細ページのURL', type: 'url', required: false, maxLength: 300, placeholder: 'https://', help: '主催者のサイトやInstagramの投稿など。申込ページと同じなら空欄で大丈夫です。' },
    ],
  },
  {
    id: 'organizer',
    title: '主催者',
    fields: [
      { name: 'organizerName', label: '主催者名（サイトに表示）', type: 'text', required: true, maxLength: 40, placeholder: '例：豊洲ピックルボールクラブ' },
      { name: 'organizerUrl', label: '主催者のサイト・SNS', type: 'url', required: false, maxLength: 300, placeholder: 'https://www.instagram.com/...', help: '主催者のページに載せます。' },
      { name: 'role', label: 'お立場', type: 'radio', required: true, options: ROLE_OPTIONS, public: false },
      { name: 'contactName', label: 'ご担当者名', type: 'text', required: true, maxLength: 40, autocomplete: 'name', public: false },
      { name: 'email', label: 'メールアドレス', type: 'email', required: true, maxLength: 120, autocomplete: 'email', public: false, help: '受付と公開のお知らせが届きます。次回から同じアドレスで申し込むと、確認なしですぐ公開されます。' },
      { name: 'emailConfirm', label: 'メールアドレス（確認）', type: 'email', required: true, maxLength: 120, confirmOf: 'email', public: false },
    ],
  },
];

export const ALL_FIELDS = SECTIONS.flatMap((s) => s.fields);

export const GUIDELINES = [
  '東京・神奈川・千葉・埼玉で開かれる、ピックルボールのイベントが対象です。',
  '誰でも参加を申し込めるもの（クローズドな身内の練習会は対象外）に限ります。',
  '物販・勧誘が主な目的のもの、内容が確認できないものは掲載を見送ることがあります。',
  '初めての主催者のイベントは、運営チームが内容を確認してから公開します（通常1〜2営業日）。2回目からは同じメールアドレスで申し込むと、すぐに公開されます。',
  '公開後に誤りや問題が見つかった場合は、運営チームの判断で修正・非公開にすることがあります。',
];
