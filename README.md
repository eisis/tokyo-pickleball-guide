# Pickleball Tokyo

首都圏（東京・神奈川・千葉・埼玉）のピックルボールコートまとめサイト。https://www.pickleball-tokyo.com/

- ドメイン：お名前.com で管理（DNS: A @ → Vercel / CNAME www → Vercel）
- ホスティング：Vercel（GitHub の main に入ると自動で公開）
- 旧URL tokyo-pickleball-guide.vercel.app は vercel.json で新ドメインへ転送

## 仕組み

```
コートや記事のファイルを追加・編集（GitHub）
   ↓ 保存（Commit）すると自動で
Vercel がサイトを組み立てる（ビルド）
   ↓ 1〜2分後
サイトに反映（一覧・詳細ページ・記事・サイトマップが全部自動更新）
```

ファイルに書き間違いがあると、Vercel のビルドが失敗し、**サイトは前の状態のまま**になります（壊れたページが公開されることはありません）。

## フォルダ構成

```
src/
  content/
    courts/      ← コート情報。1コート＝1ファイル（ここを一番よく触る）
      _template.md   コピーして使うひな形
    posts/       ← 記事。1記事＝1ファイル
  pages/         ← ページの作り（トップ・コート詳細・記事一覧・記事）
  components/    ← 部品
    CourtCard.astro     コートのカード
    CourtMap.astro      コートの地図（ピンの色＝屋内:青／屋外:緑／両方:半々）
    CourtFilters.astro  エリア・屋内外の絞り込み（カードと地図が連動）
  lib/site.ts    ← サイト名・キャッチコピー・説明文（文言を変えるときはここ）
  lib/courts.ts  ← コート共通の決まりごと（都道府県の表示名・並び順・リンクの作り方）
  layouts/       ← 全ページ共通の枠（ヘッダー・フッター・言語切替）
  styles/        ← デザイン（色・余白など）
  content.config.ts ← コート・記事に書く項目のルール
public/
  images/courts/ ← コートの写真
  pickleball-hero.mp4
scripts/         ← 自動化スクリプト（新コート探し）
.github/workflows/ ← 自動実行の設定
```

## よくある作業

### コートを追加する
1. GitHub で `src/content/courts/` を開く
2. `_template.md` を開いて中身を全部コピー
3. 「Add file」→「Create new file」→ ファイル名を `コートの英語名.md`（例: `sansan-ikebukuro.md`）にして貼り付け、中身を書き換える
4. 写真があれば `public/images/courts/` に「Add file」→「Upload files」で追加し、`image:` に `/images/courts/ファイル名` と書く
5. 地図のピン位置：Googleマップでその場所を右クリック → 一番上に出る数字（例 `35.6812, 139.7671`）をクリックでコピー → `location: { lat: 35.6812, lng: 139.7671 }` と書く
6. Commit → 1〜2分でトップのカード・地図のピン・詳細ページ `/courts/ファイル名/` が全部できる

### 新しい都道府県を増やす（埼玉・千葉など）
`src/lib/courts.ts` の `PREFECTURES` に1行、`src/content.config.ts` の `prefecture` に1語足す。絞り込みボタンはコートがある都道府県だけ自動で出る。

### 色を変える
`src/styles/global.css` の先頭（`--indoor` `--outdoor` など）を変えると、タグと地図のピンの色がまとめて変わる。

### コートを一時的に非表示にする
そのコートのファイルに `hidden: true` の1行を足す。

### 記事を書く
1. `src/content/posts/_template.md` をコピーして `記事の英語名.md` にする（ファイル名がURLになる）
2. 先頭の `---` で囲まれた部分にタイトル・説明・日付・種類（category）・タグを書き、その下に本文を書く
3. 紹介したコートのファイル名を `courts: [...]` に書くと、記事の最後にそのコートのカードが出る
4. 書きかけのときは `draft: true` を入れておけば公開されない

記事を足すだけで、次のものが自動で作られる：
- 記事一覧（`/blog/`）とカテゴリ別の一覧（`/blog/category/review/` など。記事がある種類だけ）
- タグ別の一覧（`/blog/tag/東京/` など）
- 記事ページの目次（`## 見出し` から）、読了時間、関連記事、共有ボタン、検索エンジン向けの情報
- 一覧やSNSで使う画像（`cover` がなければ本文の最初の写真 → 紹介コートの写真）

記事の種類を増やすときは `src/lib/posts.ts` の `POST_CATEGORIES` に1行、`src/content.config.ts` の `category` に1語足す。

本文の書き方（見た目のルールは全記事共通。詳しくは `_template.md`）：
- `## 見出し`（番号つきの大見出し・目次になる）、`### 小見出し`
- `**伝えたい一文**` → 黄色いマーカー（1つの見出しに1〜2か所まで）
- `> [!POINT]` `> [!TIP]` `> [!CAUTION]` `> [!NOTE]` → 色つきの箱（ポイント／ワンポイント／注意／メモ）
- 冒頭の要約は先頭部分の `points:`、コート情報の表は `facts:` に書く
- `![写真の説明](/images/posts/ファイル名.jpg)` → 説明つきの写真

### 検索できる地名を増やす
`src/lib/places.ts` の `PLACES` に「地名: [緯度, 経度]」を1行足すと、トップの検索窓でその地名から近い順に探せるようになる。

## 自動化

- **新コート探し**（毎週土曜9時）：ニュースから東京近郊（東京・神奈川・千葉・埼玉）の新しいピックルボールコートの記事を探し、候補を GitHub の Issues タブにまとめる。掲載するかは人が判断する。Actions タブの「Find new courts」→「Run workflow」で手動実行もできる。
