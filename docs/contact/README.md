# お問い合わせフォーム 導入手順

所要時間：30〜45分（DNS の反映待ちを除く）／費用：0円

## 全体像（データの流れ）

```
訪問者 → /contact（フォーム画面）
          ↓ 送信
       /api/contact（Vercel上の受付プログラム）
          ├─ ① ロボットかどうか確認（Cloudflare Turnstile）
          ├─ ② 入力チェック
          ├─ ③ 受付台帳に1行追加（Googleスプレッドシート）
          ├─ ④ info@ に通知メール（Resend）
          └─ ⑤ 問い合わせた人に自動返信（Resend）
```

## ファイル構成

| ファイル | 役割 |
|---|---|
| `src/pages/contact.astro` | フォーム画面（/contact/） |
| `src/pages/privacy.astro` | プライバシーポリシー（/privacy/） |
| `api/contact.js` | 受付プログラム |
| `api/_lib/contact-types.js` | **種別・項目の定義（今後いじるのはほぼここだけ）** |
| `docs/contact/Code.gs` | 台帳用スクリプト（スプレッドシートに貼る） |

> 設定が揃うまでは、フォームに「準備中」と表示されます。

---

## STEP 1　Resend（メール送信）の設定

1. https://resend.com で無料登録（Googleアカウントでログイン可）
2. 左メニュー **Domains → Add Domain**
   - Domain：`pickleball-tokyo.com`
   - Region：**Tokyo (ap-northeast-1)**
3. 表示される DNS レコード（通常3〜4行）をメモ
4. **お名前.com Navi → ドメイン → DNS設定/転送設定 → DNSレコード設定を利用する**
   - Resend に表示された「タイプ・ホスト名・値（・優先度）」をそのまま追加
   - ⚠️ Gmail 用にすでに入れたレコード（MX や SPF の TXT など）は**消さない・書き換えない**
   - Resend のレコードは `send.` や `resend._domainkey` で始まる名前なので、Gmail 用とはぶつかりません
5. Resend に戻って **Verify** → 緑の「Verified」になればOK（数分〜数時間）
6. 左メニュー **API Keys → Create API Key**（権限：Sending access）→ 表示されたキーを控える（`re_` で始まる。**一度しか表示されません**）

## STEP 2　Cloudflare Turnstile（迷惑投稿対策）

1. https://dash.cloudflare.com で無料登録
2. 左メニュー **Turnstile → Add widget**
   - Widget name：`Pickleball Tokyo Contact`
   - Hostnames：`pickleball-tokyo.com` を追加（動作確認用に `tokyo-pickleball-guide.vercel.app` も追加しておくと便利）
   - Widget Mode：**Managed**
3. **Site Key** と **Secret Key** を控える

## STEP 3　受付台帳（Googleスプレッドシート）

1. Googleドライブで新しいスプレッドシートを作成（名前例：`Pickleball Tokyo 問い合わせ台帳`）
2. メニュー **拡張機能 → Apps Script**
3. 最初からある中身を全部消して、`docs/contact/Code.gs` の中身を貼り付け
4. 1行目近くの `const SECRET = 'ここに合言葉を入れる';` を、適当な長い英数字に変更（例：`pbt-7k2m9xq4w8`）。**この合言葉は STEP 4 でも使います**
5. 💾 保存 → 関数選択で `testAppend` を選び **実行**
   - 初回は「承認が必要です」→ 自分のアカウントを選択 →「詳細」→「（安全ではないページ）に移動」→ 許可
   - スプレッドシートに「受付台帳」シートとテスト行ができればOK（テスト行は消してOK）
6. 右上 **デプロイ → 新しいデプロイ**
   - 種類：**ウェブアプリ**
   - 次のユーザーとして実行：**自分**
   - アクセスできるユーザー：**全員**
7. 表示された **ウェブアプリのURL**（`https://script.google.com/macros/s/.../exec`）を控える

> ※「全員」にしても、合言葉を知らない人は書き込めません。

## STEP 4　Vercel に設定値を登録

Vercel → プロジェクト → **Settings → Environment Variables** で以下を追加（Environment は Production / Preview 両方にチェック）

| Key | Value |
|---|---|
| `RESEND_API_KEY` | STEP1 のキー（`re_...`） |
| `CONTACT_TO` | `info@pickleball-tokyo.com` |
| `CONTACT_FROM` | `Pickleball Tokyo <noreply@pickleball-tokyo.com>` |
| `TURNSTILE_SITE_KEY` | STEP2 の Site Key |
| `TURNSTILE_SECRET_KEY` | STEP2 の Secret Key |
| `SHEET_WEBHOOK_URL` | STEP3 のウェブアプリURL |
| `SHEET_WEBHOOK_SECRET` | STEP3 で決めた合言葉 |

登録したら **Deployments → 最新の行の「…」→ Redeploy** を押します（設定値は再デプロイ後から反映されます）。

## STEP 5　動作確認

1. `https://www.pickleball-tokyo.com/contact/` を開く
2. 自分の別のメールアドレス（普段のGmailなど）で「その他のお問い合わせ」を送信
3. 次の3点を確認
   - [ ] 完了画面に受付番号（`PT-日付-XXXX`）が出る
   - [ ] info@ に通知メールが届き、**そのまま返信すると問い合わせ者に届く**
   - [ ] 自分の別アドレスに自動返信が届く（迷惑メールフォルダも確認）
   - [ ] 台帳に1行増え、ステータスが「未対応」になっている

うまくいかない時：Vercel → **Logs** に失敗理由が出ます（`resend:` / `sheet:` で始まる行）。

---

## サイト内からのリンク

種別を選んだ状態で開けます。

| 置く場所 | リンク先 |
|---|---|
| コート掲載募集の記事・トップのバナー | `/contact/?type=court` |
| 各コートページ下部「情報の誤りを報告」 | `/contact/?type=fix` |
| フッター「お問い合わせ」 | `/contact/` |

## 運用ルール（おすすめ）

- 台帳のステータスを「未対応 → 対応中 → 完了」に更新
- 返信は通知メールにそのまま返信（info@ の Gmail から送信）
- 自動返信で「3営業日以内に連絡」と案内しているので、それを目安に

## 今後、種別を増やすとき

`api/_lib/contact-types.js` だけを編集します。

- **大会エントリー・レッスン予約を使い始める**：該当ブロックの `enabled: false` を消す（または `true` に）。大会名などの選択肢を書き換える
- **新しい種別を作る**：既存ブロックをコピーして `id`・`label`・`fields` を書き換える
- **項目を足す**：`fields` に1行追加（使える type：`text` `email` `url` `tel` `number` `select` `radio` `checkbox` `textarea`）

画面・入力チェック・通知メール・台帳は自動で追従します。

> 定員管理・先着順・参加費の決済が必要になったら、その時点で予約専用の仕組みに切り出します（受付番号・台帳・通知はそのまま流用可能）。

