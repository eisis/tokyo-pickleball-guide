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

const PREFECTURES = ['東京都', '神奈川県', '千葉県', '埼玉県'];

const TYPES = [
  {
    id: 'court',
    sheetName: 'コート掲載', // 受付台帳のタブ名
    label: 'コートを掲載したい',
    description: '施設の運営者・管理者の方へ。掲載は無料です。',
    icon: '🏓',
    subjectField: 'facilityName', // 通知メールの件名に使う項目
    autoReplyNote: '掲載にあたり、写真や詳細情報をメールでお伺いする場合があります。',
    fields: [
      { name: 'operatorType', label: 'お立場', type: 'select', required: true,
        options: ['施設運営者', 'コート所有者・管理者', '自治体・公共施設のご担当', 'その他'] },
      { name: 'facilityName', label: '施設名', type: 'text', required: true, maxLength: 100, placeholder: '〇〇スポーツセンター' },
      { name: 'prefecture', label: '都県', type: 'select', required: true, options: PREFECTURES },
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
      { name: 'courtName', label: '対象のコート名', type: 'text', required: true, maxLength: 100 },
      { name: 'fixItems', label: '修正したい項目', type: 'checkbox', required: true,
        options: ['料金', '営業時間', '予約方法', '所在地', '写真', '閉鎖・休止', 'その他'] },
      { name: 'message', label: '修正内容', type: 'textarea', required: true, maxLength: 2000,
        placeholder: '正しい情報や、情報の出典（公式URLなど）を教えてください。' },
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
