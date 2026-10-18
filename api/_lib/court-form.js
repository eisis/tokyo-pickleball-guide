// ============================================================
// コート掲載申請フォームの定義（運営者が自分で掲載・更新するためのフォーム）
// ・画面（src/pages/owners.astro）も受付API（api/court-submit.js）もこの定義を使う
// ・選択肢は { v: 保存する値, label: 画面に出す文字 } で持つ。v はコートのファイル（content.config.ts）の値と同じ
// ・項目を足すとき：ここに1行足す → court-markdown.js の toCourtData / fromCourtData に対応を足す
// ============================================================

export const PREFECTURE_OPTIONS = [
  { v: 'tokyo', label: '東京都' },
  { v: 'kanagawa', label: '神奈川県' },
  { v: 'chiba', label: '千葉県' },
  { v: 'saitama', label: '埼玉県' },
  { v: 'other', label: 'それ以外の地域' }, // 掲載エリア外：台帳に記録だけして、エリア拡大時に連絡する
];

export const CATEGORY_OPTIONS = [
  { v: 'dedicated', label: 'ピックルボール専用コート' },
  { v: 'fitness', label: 'ジム・スクール・複合スポーツ施設' },
  { v: 'public', label: '公共施設（体育館・公園など）' },
  { v: 'circle', label: 'サークル・団体の活動場所' },
];

export const ENVIRONMENT_OPTIONS = [
  { v: 'indoor', label: '屋内' },
  { v: 'outdoor', label: '屋外' },
];

export const RENTAL_OPTIONS = [
  { v: 'free', label: '無料で貸し出し' },
  { v: 'paid', label: '有料で貸し出し' },
  { v: 'available', label: '貸し出しあり（料金は施設で案内）' },
  { v: 'none', label: '貸し出しなし' },
];

export const RESERVATION_OPTIONS = [
  { v: 'online', label: 'ネット予約' },
  { v: 'line', label: 'LINE予約' },
  { v: 'phone', label: '電話予約' },
  { v: 'walkin', label: '当日受付' },
];

// 予約システム（社内用メモ bookingSystem に入る。サイトには出さない）
export const BOOKING_SYSTEM_OPTIONS = [
  'RESERVA', 'STORES予約', 'LaBOLA', 'hacomono', 'instabase', 'TableCheck', 'Coubic', 'Square予約', 'SelectType',
  '自社の予約システム', '予約システムは使っていない', 'その他',
].map((s) => ({ v: s, label: s }));

// 連携のご相談：何を相談できるかを明記する（台帳とメールで管理し、こちらから連絡して調整する）
export const COOP_OPTIONS = [
  { v: '空き状況リンク', label: '空き状況ページへのリンク掲載', note: '空き状況を一般公開しているページがあれば、コートページに「空き状況を見る」ボタンを付けます。すぐに対応できます。' },
  { v: '空き状況表示', label: '空き状況をサイト上に表示', note: '日付ごとの空きをPickleball Tokyo上で見られるようにします。予約システムからの取り込み方法をご相談します。' },
  { v: '予約システム連携', label: '予約システムとの自動連携', note: 'お使いの予約システム（API・カレンダー連携など）とつなぎ、空き状況を自動で最新にします。' },
  { v: 'サイト経由の予約', label: 'Pickleball Tokyo からの予約受付', note: 'サイト上で予約まで完結できる仕組みを準備しています。先行してご案内します。' },
  { v: 'イベント掲載', label: 'イベント・練習会・体験会の掲載', note: '大会・オープンプレー・体験会などをイベントページに載せます。' },
  { v: '記事・SNS', label: '記事・SNSでの紹介', note: '取材記事やInstagram・Xでの紹介をご相談します。' },
  { v: '広告・特集', label: '広告・特集掲載', note: '上位表示や特集ページなど、有料のメニューを検討中です。' },
];

export const COOP_TIMING_OPTIONS = [
  { v: 'soon', label: 'すぐに相談したい' },
  { v: 'later', label: '時期を見て相談したい' },
  { v: 'info', label: 'まずは情報だけほしい' },
];

export const ROLE_OPTIONS = [
  { v: 'owner', label: '施設の運営者' },
  { v: 'staff', label: '施設の管理者・スタッフ' },
  { v: 'public', label: '自治体・公共施設のご担当' },
  { v: 'player', label: '利用者（運営者ではない）' },
];
// 運営側の立場（メールの独自ドメインが公式サイトと一致すれば「運営者掲載」にする）
export const OPERATOR_ROLES = ['owner', 'staff', 'public'];

// ---------- フォーム本体 ----------
// type: text / url / email / tel / number / date / textarea / select / radio / checkbox / photos
// only: 'new' = 新規掲載のときだけ表示 / 'update' = 更新のときだけ表示
// public: false = サイトに公開されない（審査担当だけが見る）
export const SECTIONS = [
  {
    id: 'basic',
    title: '施設の基本情報',
    lead: 'コート一覧のカードと、コートの詳細ページに表示されます。',
    fields: [
      { name: 'name', label: '施設名', type: 'text', required: true, maxLength: 60, placeholder: '〇〇ピックルボールクラブ' },
      { name: 'nameEn', label: '施設名（英語表記）', type: 'text', required: false, maxLength: 80, only: 'new', placeholder: 'Marunouchi Pickleball Club',
        help: 'ページのURLと英語表示に使います。' },
      { name: 'category', label: '施設の種類', type: 'radio', required: true, options: CATEGORY_OPTIONS },
      { name: 'environment', label: '屋内 / 屋外', type: 'checkbox', required: true, options: ENVIRONMENT_OPTIONS, help: '両方ある場合は両方を選んでください。' },
      { name: 'courts', label: 'ピックルボールのコート面数', type: 'number', required: false, min: 1, max: 99 },
      { name: 'prefecture', label: '都道府県', type: 'select', required: true, options: PREFECTURE_OPTIONS,
        help: '現在は東京・神奈川・千葉・埼玉のコートを掲載しています。それ以外の地域は、掲載エリアを広げるときにご連絡します。' },
      { name: 'areaJa', label: 'エリア表示', type: 'text', required: true, maxLength: 20, placeholder: '新橋',
        help: '一覧カードに出る地名です。駅名や地域名がおすすめです。' },
      { name: 'areaEn', label: 'エリア表示（英語）', type: 'text', required: false, maxLength: 30, placeholder: 'Shimbashi' },
      { name: 'address', label: '住所', type: 'text', required: true, maxLength: 120, placeholder: '東京都港区新橋1-2-3' },
      { name: 'accessJa', label: 'アクセス', type: 'text', required: false, maxLength: 60, placeholder: '新橋駅から徒歩3分' },
      { name: 'accessEn', label: 'アクセス（英語）', type: 'text', required: false, maxLength: 100, placeholder: '3 min walk from Shimbashi Station' },
      { name: 'mapUrl', label: 'Googleマップのリンク', type: 'url', required: false, maxLength: 500, placeholder: 'https://maps.app.goo.gl/...',
        help: 'Googleマップで施設を開き「共有」→「リンクをコピー」したものを貼ってください。サイトの地図にピンが立ちます。' },
      { name: 'officialUrl', label: '公式サイト', type: 'url', required: false, maxLength: 300, placeholder: 'https://' },
      { name: 'openedAt', label: 'オープン日', type: 'date', required: false, help: 'オープンから半年間は「NEW」が付きます。' },
    ],
  },
  {
    id: 'usage',
    title: '料金・利用情報',
    lead: '公式サイトなどで公開している内容と同じものを書いてください。',
    fields: [
      { name: 'hours', label: '営業時間', type: 'text', required: false, maxLength: 60, placeholder: '7:00〜23:00' },
      { name: 'price', label: '料金の目安', type: 'text', required: false, maxLength: 80, placeholder: '1面1時間 ¥4,000〜' },
      { name: 'rentalStatus', label: 'パドル・ボールの貸し出し', type: 'radio', required: false, options: RENTAL_OPTIONS },
      { name: 'rentalNote', label: '貸し出しの内容', type: 'text', required: false, maxLength: 60, placeholder: 'パドル1本 ¥300、ボール無料' },
      { name: 'descriptionJa', label: 'ひとこと紹介', type: 'textarea', rows: 2, required: true, maxLength: 70,
        placeholder: '駅から近い屋内コート。初心者向けの体験会も毎週開いています。', help: 'コート一覧のカードに出る紹介文です（70字まで）。' },
      { name: 'descriptionEn', label: 'ひとこと紹介（英語）', type: 'textarea', rows: 2, required: false, maxLength: 160 },
      { name: 'body', label: '施設の紹介（詳しく）', type: 'textarea', rows: 6, required: false, maxLength: 1200,
        help: '詳細ページに出る文章です。設備（更衣室・シャワー・駐車場など）や、初めての方へのご案内がおすすめです。' },
    ],
  },
  {
    id: 'booking',
    title: '予約',
    lead: '「予約する」ボタンから、そのまま御社の予約ページに移動します（手数料はかかりません）。',
    fields: [
      { name: 'reservation', label: '予約方法', type: 'checkbox', required: true, options: RESERVATION_OPTIONS },
      { name: 'bookingUrl', label: '予約ページのURL', type: 'url', required: true, maxLength: 500, placeholder: 'https://',
        help: 'ネット予約がない場合は、予約方法を案内している公式ページのURLを入れてください。' },
      { name: 'availabilityUrl', label: '空き状況が見られるページのURL', type: 'url', required: false, maxLength: 500, placeholder: 'https://',
        help: 'ログインなしで空き状況を見られるページがあれば入れてください。「空き状況を見る」ボタンが付きます。' },
      { name: 'bookingSystem', label: 'お使いの予約システム', type: 'select', required: false, options: BOOKING_SYSTEM_OPTIONS, public: false,
        help: 'サイトには表示されません。空き状況の表示や予約連携のご相談に使います。' },
      { name: 'bookingSystemOther', label: '予約システムの名前', type: 'text', required: false, maxLength: 60, public: false, showIf: { bookingSystem: ['その他'] } },
    ],
  },
  {
    id: 'photos',
    title: '写真',
    lead: '1枚目がメインの写真になります。コートが写っている明るい写真がおすすめです。',
    fields: [
      { name: 'photos', label: '写真（3枚まで）', type: 'photos', required: false, max: 3,
        help: 'スマホの写真をそのまま選べます。サイズは自動で調整します。' },
      { name: 'photoRights', label: '写真の権利', type: 'checkbox', required: false, requiredIfPhotos: true,
        options: [{ v: 'ok', label: '掲載する写真は、施設が撮影したもの、または掲載の許可を得たものです' }] },
    ],
  },
  {
    id: 'coop',
    title: '空き状況・予約連携のご相談',
    lead: '任意です。相談したいことを選んでいただければ、担当から個別にご連絡して調整します。選んだ内容がサイトに公開されることはありません。',
    fields: [
      { name: 'coop', label: '相談したいこと', type: 'checkbox', required: false, options: COOP_OPTIONS, public: false, wide: true },
      { name: 'coopTiming', label: 'ご相談の時期', type: 'radio', required: false, options: COOP_TIMING_OPTIONS, public: false, showIf: { coop: '*' } },
      { name: 'coopNote', label: 'ご相談の内容・ご要望', type: 'textarea', rows: 3, required: false, maxLength: 1000, public: false, showIf: { coop: '*' } },
    ],
  },
  {
    id: 'contact',
    title: 'ご担当者',
    lead: '審査の連絡と、掲載完了のお知らせに使います。サイトには公開されません。',
    fields: [
      { name: 'role', label: 'お立場', type: 'radio', required: true, options: ROLE_OPTIONS, public: false },
      { name: 'org', label: '会社名・団体名', type: 'text', required: false, maxLength: 100, public: false },
      { name: 'contactName', label: 'お名前', type: 'text', required: true, maxLength: 60, autocomplete: 'name', public: false, placeholder: '山田 太郎' },
      { name: 'email', label: 'メールアドレス', type: 'email', required: true, maxLength: 120, autocomplete: 'email', public: false, placeholder: 'you@example.com',
        help: '施設の公式サイトと同じドメインのメールアドレスだと、「運営者掲載」の確認がスムーズです。' },
      { name: 'emailConfirm', label: 'メールアドレス（確認用）', type: 'email', required: true, maxLength: 120, autocomplete: 'email', public: false, confirmOf: 'email', placeholder: 'もう一度入力してください' },
      { name: 'phone', label: '電話番号', type: 'tel', required: false, maxLength: 20, autocomplete: 'tel', public: false },
      { name: 'message', label: '審査担当へのメッセージ', type: 'textarea', rows: 3, required: false, maxLength: 1000, public: false },
    ],
  },
];

export const ALL_FIELDS = SECTIONS.flatMap((s) => s.fields);

// 写真の上限（画面で長辺1600pxのJPEGに縮めてから送る。Vercel の受信上限4.5MBに3枚収まる大きさ）
export const PHOTO_LIMIT = { max: 3, maxBytes: 1_000_000, maxEdge: 1600 };

// 掲載基準（画面に表示し、同意してもらう）
export const GUIDELINES = [
  'ピックルボールができる施設で、一般の方が予約・利用できること（会員制の場合は入会方法が公開されていること）。',
  '料金・営業時間などは、公式サイトなどで公開している内容と一致していること。',
  '写真は施設のもので、掲載の権利があること。',
  '内容を確認のうえ掲載します。表現を整えたり、掲載を見送ったりする場合があります。',
];
