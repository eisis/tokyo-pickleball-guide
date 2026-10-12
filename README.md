# Tokyo & Kanagawa Pickleball Court Guide

東京・神奈川のピックルボールコートまとめサイト。https://tokyo-pickleball-guide.vercel.app/

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
1. `src/content/posts/` に `記事の英語名.md` を作る（既存の記事を参考に）
2. 先頭の `---` で囲まれた部分にタイトル・説明・日付を書き、その下に本文を書く
3. 紹介したコートのファイル名を `courts: [...]` に書くと、記事の最後にそのコートのカードが出る
4. 書きかけのときは `draft: true` を入れておけば公開されない

本文の書き方（Markdown）：`## 見出し`、`- 箇条書き`、`**太字**`、`[リンク文字](URL)`

## 自動化

- **新コート探し**（毎週土曜9時）：ニュースから東京・神奈川周辺の新しいピックルボールコートの記事を探し、候補を GitHub の Issues タブにまとめる。掲載するかは人が判断する。Actions タブの「Find new courts」→「Run workflow」で手動実行もできる。
