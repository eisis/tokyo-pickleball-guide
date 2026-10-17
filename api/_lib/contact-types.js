// ============================================================
// お問い合わせ種別の定義（ここを編集すれば種別・項目を増やせます）
// ・画面（src/pages/contact.astro）もサーバー（api/contact.js）もこの定義を使います
// ・新しい種別を追加 → TYPES に1ブロック足すだけ
// ・一時的に隠したい種別 → enabled: false
// ============================================================

// 全種別共通の項目
const COMMON_FIELDS = [
  { name: 'name', label: 'お名前', type: 'text', required: true, maxLength: 60, autocomplete: 'name', placeholder: '山田 太郎' },
  { name: 'email', label: 'メールアドレス', type: 'email', required: true, maxLength: 120, autocomplete: 'email', placeholder: 'you@example.com' },
  // 打ち間違い防止の確認欄。confirmOf の項目と一致するかチェックし、メール・台帳には出さない
  { name: 'emailConfirm', label: 'メールアドレス（確認用）', type: 'email', required: true, maxLength: 120, autocomplete: 'email',
    placeholder: 'もう一度入力してください', confirmOf: 'email' },
];

// 都道府県：いま掲載しているエリアを先頭にして、見出し付きのグループで表示する
const PREFECTURE_GROUPS = [
  { label: '現在の掲載エリア', options: ['東京都', '神奈川県', '千葉県', '埼玉県'] },
  { label: '関東・近郊', options: ['茨城県', '栃木県', '群馬県', '山梨県', '静岡県'] },
  { label: 'その他の地域', options: [
    '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
    '新潟県', '富山県', '石川県', '福井県', '長野県', '岐阜県', '愛知県', '三重県',
    '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県',
    '鳥取県', '島根県', '岡山県', '広島県', '山口県',
    '徳島県', '香川県', '愛媛県', '高知県',
    '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県',
  ] },
];
const PREFECTURES = PREFECTURE_GROUPS.flatMap((g) => g.options);

const TYPES = [
  {
    id: 'court',
    sheetName: 'コート掲載', // 受付台帳のタブ名
    label: 'コートを掲載したい',
    description: '施設の運営者・管理者の方へ。基本掲載は無料です。',
    icon: '🏓',
    subjectField: 'facilityName', // 通知メールの件名に使う項目
    autoReplyNote: '掲載にあたり、写真や詳細情報をメールでお伺いする場合があります。',
    fields: [
      { name: 'operatorType', label: 'お立場', type: 'select', required: true,
        options: ['施設運営者', 'コート所有者・管理者', '自治体・公共施設のご担当', 'その他'] },
      { name: 'facilityName', label: '施設名', type: 'text', required: true, maxLength: 100, placeholder: '〇〇スポーツセンター' },
      { name: 'prefecture', label: '都道府県', type: 'select', required: true, options: PREFECTURES, groups: PREFECTURE_GROUPS,
        help: '現在は東京・神奈川・千葉・埼玉を中心に掲載しています。その他の地域も今後の掲載候補として受け付けています。' },
      { name: 'city', label: '市区町村', type: 'text', required: true, maxLength: 60, placeholder: '港区' },
      { name: 'officialUrl', label: '公式サイトURL', type: 'url', required: false, maxLength: 300, placeholder: 'https://' },
      { name: 'courts', label: 'コート面数', type: 'number', required: false, min: 1, max: 99 },
      { name: 'environment', label: '屋内 / 屋外', type: 'radio', required: false, options: ['屋内', '屋外', '両方'] },
      { name: 'booking', label: '予約方法', type: 'text', required: false, maxLength: 200, placeholder: '公式サイト / 電話 / 予約アプリ など' },
      { name: 'availabilityCoop', label: '空き状況の掲載へのご協力', type: 'radio', required: false,
        options: ['協力できる', '検討したい', '難しい'],
        help: '将来、各コートの空き状況をサイトに載せる予定です。' },
      { name: 'photos', label: '写真のご提供', type: 'radio', required: false, options: ['提供できる', '未定'] },
      { name: 'message', label: 'その他・ご要望', type: 'textarea', required: false, maxLength: 2000 },
    ],
  },
  {
    id: 'fix',
    sheetName: '情報修正', // 受付台帳のタブ名
    label: '掲載情報の修正',
    description: '料金・営業時間などの誤りや閉鎖のご連絡。',
    icon: '✏️',
    subjectField: 'courtName',
    fields: [
      { name: 'courtName', label: '対象のコート名・イベント名', type: 'text', required: true, maxLength: 100 },
      { name: 'fixItems', label: '修正したい項目', type: 'checkbox', required: true,
        options: ['料金', '営業時間', '予約方法', 'レンタル', '所在地', '写真', 'イベントの日程・内容', '閉鎖・休止', 'その他'] },
      { name: 'message', label: '修正内容', type: 'textarea', required: true, maxLength: 2000,
        placeholder: '正しい情報や、情報の出典（公式URLなど）を教えてください。' },
    ],
  },
  {
    id: 'event',
    sheetName: 'イベント掲載', // 受付台帳のタブ名
    label: 'イベントを掲載したい',
    description: '大会・練習会・体験会の主催者の方へ。掲載は無料です。',
    icon: '📅',
    subjectField: 'eventName',
    autoReplyNote: '内容を確認のうえ、イベントページに掲載します。確認のためご連絡する場合があります。',
    fields: [
      { name: 'organizerName', label: '主催者名・団体名', type: 'text', required: true, maxLength: 100 },
      { name: 'eventName', label: 'イベント名', type: 'text', required: true, maxLength: 120 },
      { name: 'eventType', label: '種類', type: 'radio', required: true, options: ['大会', '練習会・オープンプレー', '体験会', 'レッスン', 'その他'] },
      { name: 'eventDates', label: '開催日・時間', type: 'text', required: true, maxLength: 200, placeholder: '例：11月23日（日）10:00〜13:00 ／ 毎週土曜 9:00〜11:00' },
      { name: 'venue', label: '会場', type: 'text', required: true, maxLength: 150, placeholder: '施設名・住所' },
      { name: 'prefecture', label: '都道府県', type: 'select', required: true, options: PREFECTURES, groups: PREFECTURE_GROUPS },
      { name: 'level', label: '対象', type: 'radio', required: false, options: ['初心者向け', 'どなたでも', '中級以上', '上級'] },
      { name: 'price', label: '参加費', type: 'text', required: false, maxLength: 100, placeholder: '例：1人 2,000円' },
      { name: 'eventUrl', label: '詳細・申込ページのURL', type: 'url', required: false, maxLength: 300, placeholder: 'https://' },
      { name: 'message', label: 'その他・補足', type: 'textarea', required: false, maxLength: 2000 },
    ],
  },
  {
    id: 'other',
    sheetName: 'その他', // 受付台帳のタブ名
    label: 'その他のお問い合わせ',
    description: '取材・協業・広告・練習会など。',
    icon: '💬',
    subjectField: 'topic',
    fields: [
      { name: 'topic', label: 'ご用件', type: 'select', required: true,
        options: ['取材・メディア', '協業・提携', '広告掲載', '練習会・大会', 'サイトへのご意見', 'その他'] },
      { name: 'organization', label: '会社名・団体名', type: 'text', required: false, maxLength: 100 },
      { name: 'message', label: 'お問い合わせ内容', type: 'textarea', required: true, maxLength: 3000 },
    ],
  },

  // ---- 将来の拡張例（enabled: true にすると表示されます）----
  {
    id: 'tournament',
    sheetName: '大会エントリー', // 受付台帳のタブ名
    enabled: false,
    label: '大会エントリー',
    description: '大会への参加申し込み。',
    icon: '🏆',
    subjectField: 'tournament',
    fields: [
      { name: 'tournament', label: '大会名', type: 'select', required: true, options: ['（大会名をここに）'] },
      { name: 'category', label: '種目', type: 'radio', required: true, options: ['シングルス', 'ダブルス', 'ミックスダブルス'] },
      { name: 'partner', label: 'ペアのお名前', type: 'text', required: false, maxLength: 60 },
      { name: 'level', label: 'レベル', type: 'select', required: true, options: ['初心者', '初級', '中級', '上級'] },
      { name: 'phone', label: '当日連絡先（電話）', type: 'tel', required: true, maxLength: 20 },
      { name: 'message', label: '備考', type: 'textarea', required: false, maxLength: 1000 },
    ],
  },
  {
    id: 'lesson',
    sheetName: 'レッスン予約', // 受付台帳のタブ名
    enabled: false,
    label: 'レッスン予約',
    description: 'レッスン・体験会のお申し込み。',
    icon: '🎾',
    subjectField: 'lesson',
    fields: [
      { name: 'lesson', label: 'レッスン', type: 'select', required: true, options: ['（レッスン名をここに）'] },
      { name: 'people', label: '人数', type: 'number', required: true, min: 1, max: 20 },
      { name: 'experience', label: '経験', type: 'radio', required: true, options: ['未経験', '経験あり'] },
      { name: 'message', label: '備考', type: 'textarea', required: false, maxLength: 1000 },
    ],
  },
];

function getType(id) {
  return TYPES.find((t) => t.id === id && t.enabled !== false) || null;
}

export { COMMON_FIELDS, TYPES, getType };
