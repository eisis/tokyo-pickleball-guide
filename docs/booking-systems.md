# 掲載コートの予約システム一覧（社内用）

予約連携・空き状況掲載の交渉先を決めるための台帳。各コートのファイルの `bookingSystem` が元データで、ここはその要約。
判定方法は、サイトに載せている予約リンクのドメインと、公式ページの予約ボタンのリンク先。2026-10-18 時点。

## 予約システム別

| 予約システム | 施設 |
|---|---|
| RESERVA | ピックルボールワン銀座新橋、VIPインドアピックルボールクラブ東陽町 |
| LaBOLA | KPI PARK、THE PICKLE BANG THEORY |
| STORES予約 | OCEAN PICKLE CLUB 鶴見 |
| hacomono | Pickle9 |
| instabase | ゴールドジム千葉ニュータウン |
| TableCheck | SEIBU FAST SPORTS FIELD 品川 |
| LINE（手動受付） | ときがわピックルボール |
| サービス名を特定できていない | Pacific PICKLE CLUB（resv.jp）、WELL PICKLE CLUB（aero.lan.jp）、Pickle K 若葉台（reserve.andpickle.jp）、Sansan池袋（reserve.sansan-pickleball.com） |
| 未調査 | TOKYO TOWER（公式ページ取得不可）、PICKLR 豊洲・幕張、PICKLEBALL PARK TOYOSU（予約ページ未掲載） |

## 交渉の優先度の考え方

1. 同じシステムを使う施設が複数あるもの（RESERVA・LaBOLA）は、システム会社と1回話せば複数施設につながる。空き状況の埋め込みや送客連携の相談先として最優先。
2. 予約ページの空き状況を一般公開しているもの（ピックルボールワン銀座新橋は availability ページあり）は、施設の同意を得て空き状況へのリンク掲載から始める。
3. LINE・電話など手動受付の施設は、将来の自前予約受付（無料提供）の候補。
4. 送客数は台帳の「送客ログ」タブと GA4 の `court_link_click` で施設別に数えて、交渉資料に使う。
