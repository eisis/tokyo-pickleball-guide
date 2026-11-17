"""投稿18 ベン・ジョンズ特集（7枚・雑誌の選手ファイル風、白黒写真＋蛍光1色）。
使い方: python3 benjohns.py 出力先フォルダ(絶対パス) [ページ番号...]
同じフォルダに fonts/Anton.ttf と img/cover_bw.jpg・alw_bw.jpg・act_bw.jpg を置く（素材はリポジトリ外）。"""
import sys, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
INK, PAPER, ACC = "#0F0F0F", "#F1EEE8", "#D8FF3A"
N = 7

CSS = f"""
@font-face {{ font-family: Anton; src: url('file://{HERE}/fonts/Anton.ttf'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; overflow:hidden; position:relative;
  font-family:'Noto Sans CJK JP'; }}
.dark {{ background:{INK}; color:{PAPER}; }}
.light {{ background:{PAPER}; color:{INK}; }}
.an {{ font-family:Anton; letter-spacing:1px; }}
.kick {{ font-family:Anton; font-size:26px; letter-spacing:6px; }}
.rule {{ height:2px; background:currentColor; opacity:.9; }}
.top {{ position:absolute; left:64px; right:64px; top:56px; display:flex;
  justify-content:space-between; align-items:center; }}
.foot {{ position:absolute; left:64px; right:64px; bottom:48px; display:flex;
  justify-content:space-between; font-family:Anton; font-size:22px; letter-spacing:4px; opacity:.55; }}
.credit {{ font-size:20px; letter-spacing:1px; opacity:.6; }}
.grain {{ position:absolute; inset:0; pointer-events:none; opacity:.08;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='200' height='200' filter='url(%23n)'/></svg>"); }}
"""

def page(i, cls, inner):
    foot = f'<div class="foot"><span>PICKLEBALL TOKYO</span><span>{i} / {N}</span></div>'
    return f'<html><head><style>{CSS}</style></head><body class="{cls}">{inner}{foot}</body></html>'

def img(n): return f"file://{HERE}/img/{n}"

P = {}

# 1 表紙：モノクロの顔、下に巨大な名前、コピーは1行
P[1] = ("dark", f"""
<img src="{img('cover_bw.jpg')}" style="position:absolute;left:0;top:80px;width:1080px;height:1180px;object-fit:cover;object-position:50% 20%;-webkit-mask-image:linear-gradient(transparent,#000 180px);">
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,15,15,.92) 0%,rgba(15,15,15,.6) 9%,rgba(15,15,15,0) 22%,rgba(15,15,15,0) 55%,{INK} 84%);"></div>
<div class="grain"></div>
<div class="top"><span class="kick">PLAYER FILE — 01</span><span class="credit">Photo: PPA Tour Asia</span></div>
<div style="position:absolute;left:56px;right:56px;top:905px;">
  <div class="an" style="font-size:212px;line-height:.86;letter-spacing:-2px;">BEN JOHNS</div>
  <div style="display:flex;align-items:center;gap:22px;margin-top:30px;">
    <span style="width:46px;height:6px;background:{ACC};"></span>
    <span style="font-size:44px;font-weight:700;">99大会に出て、99回の表彰台。</span></div>
</div>""")

# 2 はじまり：紙の地に年号、静かな文章
P[2] = ("light", f"""
<div class="top"><span class="kick">ORIGIN</span><span class="kick" style="opacity:.5;">FLORIDA, 2016</span></div>
<div style="position:absolute;left:64px;right:64px;top:110px;"><div class="rule"></div></div>
<div style="position:absolute;left:52px;top:170px;" class="an"><span style="font-size:330px;line-height:.85;">2016</span></div>
<div style="position:absolute;left:64px;right:64px;top:500px;">
  <div style="font-size:52px;font-weight:900;line-height:1.35;">王者の原点は、兄の練習相手。</div>
  <div style="font-size:32px;line-height:1.75;margin-top:16px;color:#333;">プロを目指す兄のボールを、<br>ひたすら打ち返したテニス少年。</div>
  <div style="font-size:52px;font-weight:900;line-height:1.35;margin-top:44px;">転機は17歳、フロリダ。</div>
  <div style="font-size:32px;line-height:1.75;margin-top:16px;color:#333;">家族旅行先、兄がテニスに汗を流す隣のコート。<br>試しに握ったパドル。<br>わずか1か月後、プロの大会で5位。</div>
</div>
<div style="position:absolute;left:64px;right:64px;bottom:120px;"><div class="rule" style="height:1px;opacity:.4;"></div></div>
""")

# 3 数字：2x2の静かなグリッド
U = lambda t: f'<span style="font-family:Noto Sans CJK JP;font-weight:900;font-size:50px;margin:0 8px 0 6px;">{t}</span>'
cells = [("187" + U("回"), "PPAツアーの優勝", "これまでの通算"),
         ("99" + U("回") + "/99" + U("大会"), "メダルを取った回数", "出場した99大会、すべてで表彰台"),
         ("108" + U("連勝"), "シングルス", "1試合も負けずに勝ち続けた"),
         ("45" + U("勝") + "0" + U("敗"), "昨季の男子ダブルス", "8大会連続優勝は記録")]
grid = "".join(
    f'<div style="padding:40px 0 0 {0 if k % 2 == 0 else 40}px;'
    f'{"border-left:1px solid rgba(241,238,232,.25);" if k % 2 else ""}">'
    f'<div class="an" style="font-size:{140 if k in (0, 2) else 112}px;line-height:1;white-space:nowrap;'
    f'{"color:" + ACC + ";" if k == 0 else ""}">{n}</div>'
    f'<div style="font-size:38px;font-weight:900;margin-top:22px;">{t}</div>'
    f'<div style="font-size:26px;margin-top:10px;opacity:.7;">{d}</div></div>'
    for k, (n, t, d) in enumerate(cells))
P[3] = ("dark", f"""
<div class="top"><span class="kick">BY THE NUMBERS</span><span class="kick" style="opacity:.5;">AS OF SEP 2026</span></div>
<div style="position:absolute;left:64px;right:64px;top:110px;"><div class="rule"></div></div>
<div style="position:absolute;left:64px;right:64px;top:170px;font-size:60px;font-weight:900;line-height:1.35;">
  記録が、<br>王者を語る。</div>
<div style="position:absolute;left:64px;right:64px;top:430px;display:grid;grid-template-columns:1fr 1fr;row-gap:70px;">
  <div style="grid-column:1/3;" class="rule"></div>
  {grid[:grid.index('<div style="padding', 10)]}
  {grid[grid.index('<div style="padding', 10):]}
</div>

""")

# 4 素顔
P[4] = ("light", f"""
<div class="top"><span class="kick">OFF THE COURT</span><span class="kick" style="opacity:.5;">3 THINGS</span></div>
<div style="position:absolute;left:64px;right:64px;top:110px;"><div class="rule"></div></div>
<div style="position:absolute;left:64px;right:64px;top:170px;font-size:64px;font-weight:900;line-height:1.35;">コートの外の、<br>王者の素顔。</div>
<div style="position:absolute;left:64px;right:64px;top:420px;"><div style="display:flex;gap:34px;padding:42px 0;border-top:1px solid rgba(15,15,15,.25);">
  <div class="an" style="font-size:56px;line-height:1;width:70px;">01</div>
  <div><div style="font-size:46px;font-weight:900;line-height:1.3;">パドルは、自分で設計。</div>
  <div style="font-size:30px;line-height:1.7;margin-top:12px;color:#333;">大学で材料工学を専攻。自分の名を冠したパドルは、<br>素材も寸法も形も、自ら指定した。</div></div></div><div style="display:flex;gap:34px;padding:42px 0;border-top:1px solid rgba(15,15,15,.25);">
  <div class="an" style="font-size:56px;line-height:1;width:70px;">02</div>
  <div><div style="font-size:46px;font-weight:900;line-height:1.3;">素性を隠して、カード対戦。</div>
  <div style="font-size:30px;line-height:1.7;margin-top:12px;color:#333;">11〜17歳はマジック：ザ・ギャザリングに没頭。<br>ネットの対戦相手は、王者だとは知らない。</div></div></div><div style="display:flex;gap:34px;padding:42px 0;border-top:1px solid rgba(15,15,15,.25);">
  <div class="an" style="font-size:56px;line-height:1;width:70px;">03</div>
  <div><div style="font-size:46px;font-weight:900;line-height:1.3;">王者の好物は、魚形クラッカー。</div>
  <div style="font-size:30px;line-height:1.7;margin-top:12px;color:#333;">子どもの頃から、ゴールドフィッシュが<br>やめられない。</div></div></div></div>
""")

# 5 言葉
P[5] = ("dark", f"""
<img src="{img('act_bw.jpg')}" style="position:absolute;right:-130px;top:130px;width:760px;height:1143px;object-fit:cover;-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 160px,#000 70%,transparent 100%);">
<div style="position:absolute;inset:0;background:linear-gradient(90deg,{INK} 44%,rgba(15,15,15,.8) 56%,rgba(15,15,15,.1) 88%);"></div>
<div class="grain"></div>
<div class="top"><span class="kick">IN HIS WORDS</span><span class="kick" style="opacity:.5;">PICKLEBALL MAGAZINE, 2025</span></div>
<div style="position:absolute;left:64px;right:64px;top:110px;"><div class="rule"></div></div>
<div class="credit" style="position:absolute;right:64px;top:130px;">Photo: Major League Pickleball</div>
<div class="an" style="position:absolute;left:52px;top:300px;font-size:260px;line-height:1;color:{ACC};">“</div>
<div style="position:absolute;left:64px;right:64px;top:560px;">
  <div style="font-size:80px;font-weight:900;line-height:1.35;text-shadow:0 2px 20px rgba(0,0,0,.6);">全部の試合に、<br>勝てると思っている。</div>
  <div class="an" style="font-size:40px;letter-spacing:2px;margin-top:40px;opacity:.6;">"I KNOW I CAN WIN EVERY MATCH."</div>
  <div style="font-size:30px;line-height:1.7;margin-top:46px;opacity:.8;">「衰えた」の声も、意に介さない。<br>試合前の心のルーティンすら、持たない。</div>
</div>
""")

# 6 いま：モノクロの2人、短い言葉
P[6] = ("dark", f"""
<img src="{img('alw_bw.jpg')}" style="position:absolute;left:0;top:130px;width:1080px;height:740px;object-fit:cover;object-position:50% 0%;">
<div style="position:absolute;left:0;right:0;top:680px;height:200px;background:linear-gradient(rgba(15,15,15,0),{INK});"></div>
<div class="grain"></div>
<div class="top"><span class="kick">NOW</span><span class="credit">Photo: PPA Tour (Texas Open)</span></div>
<div style="position:absolute;left:64px;right:64px;top:880px;">
  <div style="font-size:64px;font-weight:900;line-height:1.3;">王者は、まだ頂にいる。</div>
  <div style="font-size:34px;line-height:1.7;margin-top:22px;opacity:.85;">
    11月、世界選手権。<br>アンナ・リー・ウォーターズとミックスを制覇。<br>
    16大会連続優勝の記録を持つ、最強のペア。</div>
</div>""")

# 7 締め
P[7] = ("light", f"""
<div class="top"><span class="kick">END OF FILE 01</span><span class="kick" style="opacity:.5;">NEXT : FILE 02</span></div>
<div style="position:absolute;left:64px;right:64px;top:110px;"><div class="rule"></div></div>
<div style="position:absolute;left:64px;right:64px;top:250px;">
  <div style="font-size:76px;font-weight:900;line-height:1.4;">始まりは、<br>旅先で見つけた<br>1面のコート。</div>
  <div style="font-size:36px;line-height:1.8;margin-top:40px;color:#333;">王者の最初の1球も、<br>偶然の出会いから生まれた。</div>
  <div style="display:inline-block;margin-top:56px;font-size:60px;font-weight:900;border-bottom:8px solid {ACC};padding-bottom:4px;">次は、あなたの1球目。</div>
</div>
<div style="position:absolute;left:64px;right:64px;top:1010px;display:grid;grid-template-columns:1fr 1fr;border-top:2px solid {INK};">
  <div style="padding:30px 24px 0 0;">
    <div class="kick" style="font-size:22px;opacity:.6;">FIND A COURT</div>
    <div style="font-size:30px;font-weight:700;margin-top:12px;line-height:1.5;">近くのコートは<br>プロフィールのリンクから</div></div>
  <div style="padding:30px 0 0 32px;border-left:1px solid rgba(15,15,15,.3);">
    <div class="kick" style="font-size:22px;opacity:.6;">FOLLOW</div>
    <div style="font-size:30px;font-weight:700;margin-top:12px;line-height:1.5;">次の選手ファイルは<br>@pickleballtokyo で</div></div>
</div>
""")

def main():
    out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    pages = [int(a) for a in sys.argv[2:]] or list(P)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i in pages:
            cls, inner = P[i]
            f = out / f"_p{i}.html"; f.write_text(page(i, cls, inner), encoding="utf-8")
            pg.goto(f"file://{f}"); pg.wait_for_timeout(300)
            pg.screenshot(path=str(out / f"bj3_{i}.jpg"), type="jpeg", quality=92); f.unlink()
        b.close()

if __name__ == "__main__":
    main()
