---
# ↓ このファイルをコピーして「コートの英語名.md」（例: sansan-ikebukuro.md）で保存し、中身を書き換える
# 「_」で始まるファイルはサイトに表示されません
name: 施設名
area: { ja: エリア名, en: Area name }
prefecture: tokyo            # tokyo / kanagawa / saitama / chiba
environment: [indoor]        # [indoor] / [outdoor] / [indoor, outdoor]
category: dedicated          # dedicated=専用コート / fitness=ジム・スクール / public=公共施設 / circle=サークル
courts: 2                    # 面数（わからなければこの行を消す）
address: 東京都〇〇区〇〇1-2-3
access: { ja: 〇〇駅から徒歩5分, en: 5 min walk from 〇〇 Station }
hours: "9:00〜22:00"
price: 1時間 ¥5,000〜
rental: { status: free, note: パドル・ボール }   # 道具の貸し出し：free=無料 / paid=有料 / available=あり（料金不明） / none=なし。確認できなければこの行を消す
reservation: [online]        # 予約方法：online=ネット / line=LINE / phone=電話 / walkin=当日受付（複数可）。確認できなければこの行を消す
description:
  ja: カードに出る短い紹介文（2文くらい）
  en: Short description in English
officialUrl: https://example.com/   # 施設の公式サイト。書いておくと、そこのシェア用画像を自動で取ってくる
# image: の行は書かなくてOK（自動で追加される）。自分で用意した写真を使うときだけ書く
booking: { url: "https://example.com/", label: book }   # label: book=予約する / info=詳細を見る
bookingSystem: "RESERVA"                                # 社内用メモ：予約に使っているシステム（サイトには出さない・分からなければ消す）
availabilityUrl: https://example.com/availability       # 空き状況ページがなければこの行を消す
location: { lat: 35.6812, lng: 139.7671 }   # 地図のピン位置。Googleマップで場所を右クリック→一番上の数字をコピー（左が lat、右が lng）
mapQuery: Googleマップで検索する名前
openedAt: 2026-10-01         # オープン日（半年以内なら NEW が付く）。不明なら消す
updatedAt: 2026-10-12        # 情報を確認した日
sources:
  - https://情報源のURL
---

詳細ページに出る本文。施設の特徴や、行ってみた感想などを自由に書けます。
