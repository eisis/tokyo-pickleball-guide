// ============================================================
// お問い合わせ種別の定義（ここを編集すれば種別・項目を増やせます）
// ・画面（src/pages/contact.astro）もサーバー（api/contact.js）もこの定義を使います
// ・新しい種別を追加 → TYPES に1ブロック足すだけ
// ・一時的に隠したい種別 → enabled: false
// ・専用ページで受け付ける種別 → href: '/パス/'（カードを押すとそのページへ移動する）
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
    // コートの掲載・更新は専用ページ（/owners/）で受け付ける。ここは入口のカードだけ
    id: 'court',
    label: 'コートを掲載・更新したい',
    description: '施設の運営者の方へ。専用フォームから掲載内容を直接お送りいただけます。',
    icon: '🏓',
    href: '/owners/',
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
    description: '大会・練習会・体験会の主催者の方へ。',
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
    // マイパドルの申し込み（/my-paddle/ のボタンから、デザインを入れた状態で開く）
    id: 'paddle',
    sheetName: 'マイパドル', // 受付台帳のタブ名
    label: 'マイパドルを申し込む',
    description: '自分だけのデザインのパドルを1本から。',
    icon: '🎨',
    subjectField: 'design',
    autoReplyNote: '印刷用に整えた見本と、お支払い金額・振込先をメールでお送りします。ご自分のイラストやロゴを使いたい場合は、このメールに画像を添付して返信してください。',
    fields: [
      { name: 'design', label: 'デザイン（柄・色・名前）', type: 'text', required: true, maxLength: 120,
        placeholder: '例：ドット／ピーチ／HANA　（自作のイラストを使う場合は「自作イラスト」）',
        pattern: '^[^<>{}]*$', patternMessage: '< > { } の記号は使えません。' },
      { name: 'quantity', label: '本数', type: 'number', required: true, min: 1, max: 20 },
      { name: 'phone', label: '電話番号（配送用）', type: 'tel', required: true, maxLength: 20, autocomplete: 'tel',
        placeholder: '09012345678', normalize: 'digits', pattern: '^0\\d{9,10}$', patternMessage: '0から始まる10桁か11桁の番号を入力してください。' },
      { name: 'postal', label: '郵便番号', type: 'text', required: true, maxLength: 10, autocomplete: 'postal-code',
        placeholder: '1234567', normalize: 'digits', pattern: '^\\d{7}$', patternMessage: '7桁の数字で入力してください。' },
      { name: 'shipPref', label: '都道府県', type: 'select', required: true, options: PREFECTURES, groups: PREFECTURE_GROUPS, autocomplete: 'address-level1' },
      { name: 'address', label: '市区町村・番地', type: 'text', required: true, maxLength: 120, autocomplete: 'address-line1',
        placeholder: '〇〇区〇〇1-2-3', pattern: '[0-9０-９一二三四五六七八九十丁]', patternMessage: '番地まで入力してください。' },
      { name: 'building', label: '建物名・部屋番号', type: 'text', required: false, maxLength: 100, autocomplete: 'address-line2',
        placeholder: '〇〇マンション101' },
      { name: 'message', label: 'ご要望', type: 'textarea', required: false, maxLength: 2000,
        placeholder: '色の調整や、名前の書体の希望など' },
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
  return TYPES.find((t) => t.id === id && t.enabled !== false && !t.href) || null;
}

export { COMMON_FIELDS, TYPES, getType };
