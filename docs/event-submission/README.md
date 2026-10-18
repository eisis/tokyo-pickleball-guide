# イベント掲載フォームのしくみ

主催者が /events/submit/ から自分でイベントを載せる仕組みです。受付は api/event-submit.js、項目の定義は api/_lib/event-form.js。

## 公開のしかた（信頼度で分ける）

1. はじめての主催者：承認待ちの PR（ブランチ event/...）ができ、info@ に通知が届く。Vercel のプレビューで確認して Merge すると公開され、申請者に公開のお知らせが届く（.github/workflows/event-review.yml → api/event-review.js）。
2. Merge と同時に src/content/organizers/ に主催者のファイルができる。`trusted: true` なら、次回から同じメールアドレスの申し込みは確認なしで main に直接反映され、すぐ公開される（info@ には「公開しました」の通知だけ届く）。
3. 即時公開したものに問題があれば、イベントのファイルに `hidden: true` を足すか削除する。主催者の即時公開を止めるときは、主催者のファイルを `trusted: false` にする。

メールアドレスはファイルに書かず、SUBMIT_SECRET 付きのハッシュ（emailKeys）だけを残す。SUBMIT_SECRET を変えると照合できなくなるので変えないこと。

## 台帳・計測

受付台帳（スプレッドシート）に「イベント掲載申請」タブが自動で作られる。イベントページの申込・詳細リンクのクリックは「送客ログ」タブに記録され、主催者ごとの送客数を出す材料になる。

## 必要な設定

コート掲載申請と同じ環境変数（GITHUB_SUBMIT_TOKEN・SUBMIT_SECRET・RESEND_API_KEY・CONTACT_TO・CONTACT_FROM・SHEET_WEBHOOK_URL・SHEET_WEBHOOK_SECRET・TURNSTILE_*）をそのまま使う。追加の設定はない。
