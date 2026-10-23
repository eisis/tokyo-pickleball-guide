# Instagram投稿の画像スクリプト

投稿の一覧・キャプション・作り方の決まり・デザインのルールは、claude.ai のプロジェクト「Pickleball」の資料 `claude/instagram-posts.md` が正本です。ここには置きません（二重管理で内容がずれるのを防ぐため）。

`scripts/` には、投稿画像を作った Python（PIL）スクリプトがあります。中のパス（SP・OUT）は作業時のものなので、使うときに書き換えてください。

- art.py：パドルとボール（3D風）の部品
- easy2.py：投稿6（人物 `front_person`・横向き `server`・光の帯・コート図）
- weekend.py：投稿5（イベント紹介カード）
- make.py：投稿1、rules.py：投稿2、start7.py・slide4.py：投稿3、us2_base.py・s1.py・s2_8.py：投稿4
- shot.py：サイトのスクリーンショット（Playwright）
