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
description:
  ja: カードに出る短い紹介文（2文くらい）
  en: Short description in English
image: /images/courts/ファイル名.png   # 写真がなければこの行を消す（🏓が表示される）
booking: { url: "https://example.com/", label: book }   # label: book=予約する / info=詳細を見る
availabilityUrl: https://example.com/availability       # 空き状況ページがなければこの行を消す
location: { lat: 35.6812, lng: 139.7671 }   # 地図のピン位置。Googleマップで場所を右クリック→一番上の数字をコピー（左が lat、右が lng）
mapQuery: Googleマップで検索する名前
openedAt: 2026-10-01         # オープン日（半年以内なら NEW が付く）。不明なら消す
updatedAt: 2026-10-12        # 情報を確認した日
sources:
  - https://情報源のURL
---

詳細ページに出る本文。施設の特徴や、行ってみた感想などを自由に書けます。
