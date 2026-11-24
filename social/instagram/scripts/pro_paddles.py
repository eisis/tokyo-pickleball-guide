"""投稿19 試作：世界のトップは、何で打っている？（パドル特集）
python3 make.py 出力先フォルダ
パドルの絵は仮（公式写真に差し替える前提）。"""
import sys, os
from playwright.sync_api import sync_playwright

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
os.makedirs(OUT, exist_ok=True)
FONT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fonts", "Anton.woff2"))

PAPER, INK, ACC, GRAY = "#F1ECE2", "#111111", "#C9F23D", "#8A857C"
N = 7
BEN = "file:///home/claude/paddles/ben.png"
BENG = "file:///home/claude/paddles/ben_glow.png"
BRAND = {"JOOLA": "#D62839", "Facolos": "#6A4C93", "Paddletek": "#1B998B", "Franklin": "#2D5DA8",
         "PIKKL": "#F18F01", "CRBN": "#3A3A3A", "adidas": "#8C8C8C", "Engage": "#2F7D4F",
         "Luzz": "#C9A227", "Friday": "#E56399", "Eleven Zero": "#5B7083"}


def img(src, w, rot=0, extra=""):
    return f'<img src="{src}" style="width:{w}px;transform:rotate({rot}deg);{extra}">'


def paddle(face, edge=None, shape="std", w=200, rot=0, frame=False):
    """汎用のパドルのシルエット（SVG）。shape: std / elong / hybrid"""
    edge = edge or "#1a1a1a"
    if shape == "elong":
        hw, hh, rx = 150, 300, 38
    elif shape == "hybrid":
        hw, hh, rx = 170, 285, 60
    else:
        hw, hh, rx = 190, 255, 70
    hl = 140  # handle length
    W, H = 220, hh + hl + 20
    x0 = (W - hw) / 2
    hx = W / 2 - 18
    fr = ""
    if frame:
        fr = f'<rect x="{x0+3}" y="13" width="{hw-6}" height="{hh-6}" rx="{rx-3}" fill="none" stroke="{ACC}" stroke-width="9"/>' \
             f'<path d="M{W/2-26},{hh+10} L{W/2-14},{hh+60} L{W/2+14},{hh+60} L{W/2+26},{hh+10}" fill="none" stroke="{ACC}" stroke-width="9" stroke-linejoin="round"/>'
    return f'''<svg viewBox="0 0 {W} {H}" style="width:{w}px;transform:rotate({rot}deg)" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="g{face[1:]}{shape}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{face}"/><stop offset="1" stop-color="{face}" stop-opacity=".82"/></linearGradient></defs>
  <rect x="{hx}" y="{hh}" width="36" height="{hl}" rx="12" fill="#222"/>
  <rect x="{hx}" y="{hh+hl-22}" width="36" height="22" rx="8" fill="#000"/>
  <path d="M{hx+4},{hh+20} h28 M{hx+4},{hh+48} h28 M{hx+4},{hh+76} h28 M{hx+4},{hh+104} h28" stroke="#3a3a3a" stroke-width="3"/>
  <rect x="{x0}" y="10" width="{hw}" height="{hh}" rx="{rx}" fill="url(#g{face[1:]}{shape})" stroke="{edge}" stroke-width="10"/>
  {fr}
</svg>'''


BASE = f"""
@font-face {{ font-family: Anton; src: url('file://{FONT}'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; font-family:'Noto Sans CJK JP'; color:{INK}; background:{PAPER}; overflow:hidden; position:relative; }}
.en {{ font-family:Anton; letter-spacing:.02em; }}
.lab {{ position:absolute; left:80px; top:70px; font-family:Anton; font-size:34px; letter-spacing:.12em; }}
.lab b {{ background:{INK}; color:{PAPER}; padding:4px 14px; font-weight:400; }}
.foot {{ position:absolute; left:80px; right:80px; bottom:48px; display:flex; justify-content:space-between;
        font-family:Anton; font-size:26px; letter-spacing:.14em; color:{GRAY}; }}
h1 {{ font-weight:900; font-size:88px; line-height:1.22; letter-spacing:-.01em; }}
.mk {{ border-bottom:14px solid {ACC}; }}
.note {{ font-size:24px; color:{GRAY}; }}
.dark {{ background:{INK}; color:{PAPER}; }}
"""


def page(n, body, dark=False):
    fcol = "#777" if dark else GRAY
    return f"""<html><head><style>{BASE}</style></head>
<body class="{'dark' if dark else ''}">{body}
<div class="foot" style="color:{fcol}"><span>PICKLEBALL TOKYO</span><span>{n}/{N} @pickleballtokyo</span></div>
</body></html>"""


slides = []

# 1 表紙
slides.append(page(1, f"""
<div style="position:absolute;inset:0;background:#0b1419"></div>
<img src="file:///home/claude/paddles/cover4_comp.png" style="position:absolute;left:194px;top:243px;width:886px;height:1107px">
<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,20,25,.96) 0%,rgba(11,20,25,.85) 14%,rgba(11,20,25,0) 30%)"></div>
<div class="lab"><b style="background:{ACC};color:{INK}">GEAR FILE — 01</b></div>
<h1 style="position:absolute;left:80px;top:150px;font-size:96px;line-height:1.18;color:#fff">世界のトップは、<br><span style="color:{ACC}">何で</span>打っている？</h1>
<div class="en" style="position:absolute;left:80px;top:500px;font-size:80px;line-height:.98;color:#fff;text-shadow:0 0 18px rgba(0,0,0,.85),0 0 6px rgba(0,0,0,.7)">TOP<br>PLAYERS'<br>PADDLES</div>
<div style="position:absolute;left:80px;top:790px;width:120px;border-top:4px solid {ACC}"></div>
<div class="en" style="position:absolute;left:80px;top:960px;font-size:72px;line-height:1;color:{ACC}">2026</div>
<div style="position:absolute;left:80px;top:1055px;font-size:34px;font-weight:900;line-height:1.5;color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.8)">男女の世界トップ10が、<br>試合で使う1本。</div>
"""))


def ranking(n, title, sub, rows):
    items = ""
    for r, name, model, col, shape, unreleased in rows:
        brand, mdl = model.split("<br>")
        c = BRAND[brand]
        pic = paddle(c, None, "std", 40) if not unreleased else \
            f'<div style="width:40px;height:70px;border:4px dashed {c};border-radius:14px"></div>'
        items += f"""<div style="display:flex;align-items:center;gap:22px;height:86px;border-top:2px solid #d9d2c4">
  <div class="en" style="font-size:52px;width:70px;text-align:right">{r}</div>
  <div style="width:44px;display:flex;justify-content:center">{pic}</div>
  <div style="width:420px;white-space:nowrap;line-height:1.2"><div style="font-size:28px;font-weight:900">{name.split("|")[0]}</div><div class="en" style="font-size:22px;color:{GRAY};letter-spacing:.04em">{name.split("|")[1].upper()}</div></div>
  <div style="flex:1;line-height:1.25"><span style="background:{c};color:#fff;font-size:21px;font-weight:700;padding:3px 12px;border-radius:20px">{brand}</span>
    <div style="font-size:21px;color:#444;margin-top:5px">{mdl}</div></div></div>"""
    return page(n, f"""
<div class="lab"><b>{title}</b></div>
<h1 style="position:absolute;left:80px;top:150px;font-size:66px">{sub}</h1>
<div style="position:absolute;left:60px;right:70px;top:300px">{items}<div style="border-top:2px solid #d9d2c4"></div></div>
<div class="note" style="position:absolute;left:80px;bottom:100px">2026年9月時点の世界ランキング上位10人／色はメーカー別／出典：The Kitchen</div>
""")


slides.append(ranking(2, "MEN'S TOP 10", "男子トップ10の、<span class='mk'>試合の1本</span>。", [
    (1, "ベン・ジョンズ|Ben Johns", "JOOLA<br>Perseus Pro V 16mm", "#C8102E", "std", False),
    (2, "ゲイブ・タルディオ|Gabe Tardio", "Facolos<br>Elite X V2.0", "#2B2B2B", "elong", False),
    (3, "クリスチャン・アルション|Christian Alshon", "Paddletek<br>Honeyfoam TKO-X", "#1F4E8C", "elong", False),
    (4, "ヘイデン・パトリキン|Hayden Patriquin", "Franklin<br>C45 Dynasty 16mm（本人モデル）", "#333333", "elong", False),
    (5, "フェデリコ・スタクスルド|Federico Staksrud", "JOOLA<br>Kosmos Pro V 16mm", "#3B3B3B", "hybrid", False),
    (6, "JW・ジョンソン|JW Johnson", "PIKKL<br>発売前のモデル", "", "", True),
    (7, "アンドレイ・ダエスク|Andrei Daescu", "CRBN<br>CRBN1 TruFoam Barrage", "#202020", "elong", False),
    (8, "CJ・クリンガー|CJ Klinger", "adidas<br>AdiPower Pro EDT 16mm", "#1d1d1d", "std", False),
    (9, "エリック・オンシンズ|Eric Oncins", "Engage<br>X2", "#2f5d50", "elong", False),
    (10, "ノエ・クリフ|Noe Khlif", "JOOLA<br>Perseus Pro V 16mm", "#2B2B2B", "std", False),
]))

slides.append(ranking(3, "WOMEN'S TOP 10", "女子トップ10の、<span class='mk'>試合の1本</span>。", [
    (1, "アンナ・リー・ウォーターズ|Anna Leigh Waters", "Franklin<br>発売前のモデル", "", "", True),
    (2, "アンナ・ブライト|Anna Bright", "JOOLA<br>Scorpeus Pro V 14mm", "#2a2a2a", "std", False),
    (3, "ジョージャ・ジョンソン|Jorja Johnson", "PIKKL<br>発売前のモデル", "", "", True),
    (4, "タイラ・ブラック|Tyra Black", "PIKKL<br>Hurricane Pro 14mm", "#3a3a5a", "hybrid", False),
    (5, "キャサリン・パレンテュー|Catherine Parenteau", "Luzz<br>Glider", "#444", "hybrid", False),
    (6, "パリス・トッド|Parris Todd", "Franklin<br>C45（本人モデル）", "#333", "elong", False),
    (7, "レイチェル・ローラバッカー|Rachel Rohrabacher", "Friday<br>Fever 102 Elongated 16mm", "#B23A48", "elong", False),
    (8, "ケイト・フェイヒー|Kate Fahey", "JOOLA<br>Agassi Pro V", "#2a2a2a", "std", False),
    (9, "ティナ・ピスニク|Tina Pisnik", "Eleven Zero<br>EZ Speed E16", "#444", "std", False),
    (10, "ケイトリン・クリスチャン|Kaitlyn Christian", "Luzz<br>Glider", "#444", "hybrid", False),
]))

# 4 JOOLA
def jcard(name, model, who):
    return f"""<div style="width:205px;text-align:center">
  <div style="height:310px;display:flex;align-items:flex-end;justify-content:center">{img("file:///home/claude/paddles/"+name+".png", 142)}</div>
  <div class="en" style="font-size:30px;margin-top:16px;line-height:1.1">{model}</div>
  <div style="font-size:22px;color:#bbb;margin-top:6px;line-height:1.4">{who}</div></div>"""


slides.append(page(4, f"""
<div class="lab"><b style="background:{PAPER};color:{INK}">MOST MEDALS</b></div>
<h1 style="position:absolute;left:80px;top:150px;font-size:80px">いちばん勝っている<br>ブランドは、</h1>
<div class="en" style="position:absolute;left:76px;top:365px;font-size:180px;line-height:1;color:{ACC}">JOOLA</div>
<div class="en" style="position:absolute;left:80px;top:565px;font-size:110px;line-height:1">32.5%</div>
<div style="position:absolute;left:500px;top:570px;font-size:34px;font-weight:700;line-height:1.5">メダルの約3分の1は、<br>JOOLAのパドルから。</div>
<div style="position:absolute;left:80px;top:695px;font-size:22px;color:#999">2026年・米国のPPAツアー10大会のメダル240個のうち（出典：The Kitchen）　画像：JOOLA</div>
<div style="position:absolute;left:80px;right:80px;top:745px;border-top:2px solid #444;padding-top:22px;font-size:32px;font-weight:900">男女トップ10の20人のうち、<span style="color:{ACC}">5人</span>がJOOLA Pro V。<span style="font-size:20px;color:#999;font-weight:400">（2026年9月時点）</span></div>
<div style="position:absolute;left:70px;right:70px;top:830px;display:flex;justify-content:space-between">
  {jcard("perseus","PERSEUS","ジョンズ／クリフ")}{jcard("kosmos","KOSMOS","スタクスルド")}{jcard("scorpeus","SCORPEUS","ブライト")}{jcard("agassi","AGASSI","フェイヒー")}</div>
""", dark=True))

# 5 王者の1本
spec = [("厚さ", "16mm"), ("重さ", "8.1オンス<br><span style='font-size:22px;color:#aaa'>約230g</span>"), ("持ち手の太さ", "4.25インチ"), ("価格", "299.95ドル<br><span style='font-size:22px;color:#aaa'>約4万8,000円</span>")]
rows = "".join(f'<div style="display:flex;justify-content:space-between;align-items:center;border-top:2px solid #555;padding:14px 0;font-size:28px"><span style="font-weight:700">{a}</span><span style="font-family:Anton,\'Noto Sans CJK JP\';font-size:34px;text-align:right;line-height:1.15">{b}</span></div>' for a, b in spec)
slides.append(page(5, f"""
<div style="position:absolute;left:180px;top:-120px;width:1000px;height:1500px;background:url('file:///home/claude/paddles/johns_bw.jpg') center/cover"></div>
<div style="position:absolute;inset:0;background:linear-gradient(90deg,#111 0%,#111 22%,rgba(17,17,17,.75) 45%,rgba(17,17,17,0) 70%)"></div>
<div style="position:absolute;inset:0;background:linear-gradient(0deg,#111 0%,rgba(17,17,17,0) 22%)"></div>
<div class="lab"><b style="background:{PAPER};color:{INK}">THE CHAMPION'S PADDLE</b></div>
<h1 style="position:absolute;left:80px;top:160px;color:#fff">王者が選んだ、<br><span class="mk">赤い縁の1本。</span></h1>
<div style="position:absolute;left:80px;width:440px;top:440px;color:#fff">
  <div class="en" style="font-size:40px;color:#999">BEN JOHNS</div>
  <div class="en" style="font-size:54px;line-height:1.05;margin:6px 0 26px">JOOLA<br>PERSEUS PRO V</div>
  {rows}<div style="border-top:2px solid #555"></div>
  <div style="font-size:26px;line-height:1.5;color:#bbb;margin-top:20px">赤は、本人モデルの色。</div>
</div>
<div style="position:absolute;right:55px;top:700px">{img(BEN, 245, 10, "filter:drop-shadow(0 12px 18px rgba(0,0,0,.6))")}</div>
<div class="note" style="position:absolute;left:80px;top:1215px;font-size:21px;color:#888">出典・画像：JOOLA公式／1ドル＝159.5円（11/24）で換算</div>
""", dark=True))

# 6 しなって戻る
slides.append(page(6, f"""
<div class="lab"><b style="background:{PAPER};color:{INK}">KINETIC FRAME</b></div>
<h1 style="position:absolute;left:80px;top:160px">打った瞬間、<br><span style="color:{ACC}">しなって戻る。</span></h1>
<div style="position:absolute;left:60px;top:400px">{img(BENG, 300)}</div>
<div style="position:absolute;left:285px;top:765px;display:flex;align-items:center;gap:12px">
  <div style="width:110px;height:4px;background:{ACC}"></div>
  <div style="background:{ACC};color:{INK};font-size:26px;font-weight:900;padding:6px 16px;border-radius:24px;white-space:nowrap">ここがしなる</div></div>
<div style="position:absolute;left:480px;right:80px;top:450px;font-size:40px;line-height:1.55;font-weight:700">
  面と持ち手のつなぎ目<br>（スロート）が、<br>わざとしなる作り。</div>
<div style="position:absolute;left:480px;right:80px;top:665px;font-size:28px;line-height:1.6;color:#bbb">
  当たるとしなって勢いをため、<br>戻る力で打ち返す。</div>
<div style="position:absolute;left:480px;right:80px;top:880px;border-left:12px solid {ACC};padding-left:34px">
  <div style="font-size:44px;font-weight:900;line-height:1.4">「速い球は、<br>パドルの先で打つ。」</div>
  <div class="en" style="font-family:Anton;font-size:30px;color:{ACC};margin-top:14px;line-height:1.3;letter-spacing:.03em">"I OFTEN HIT THE BALL TOWARDS<br>THE END OF THE PADDLE."</div><div style="font-size:26px;color:#bbb;margin-top:14px;line-height:1.5">力を入れすぎずに、回転をかけられる。<br>— ベン・ジョンズ</div></div>
<div class="note" style="position:absolute;left:80px;bottom:100px;color:#888">出典・画像：JOOLA公式　</div>
""", dark=True))

# 7 あなたの1本を見つけよう
order = ["p2", "friday", "adidas", "engage", "franklin", "luzz", "crbn", "pikkl"]
rots = [-9, 5, -4, 7, -6, 4, -7, 8]
dys = [30, 0, 35, 8, 30, 0, 32, 6]
fan = ""
for i, n in enumerate(order):
    fan += f'<div style="position:absolute;left:{52 + i*116}px;top:{dys[i]}px;height:340px;transform:rotate({rots[i]}deg);filter:drop-shadow(0 8px 10px rgba(0,0,0,.18))"><img src="file:///home/claude/paddles/mix/{n}.png" style="height:340px"></div>'

slides.append(page(7, f"""
<div class="lab"><b>FIND YOUR PADDLE</b></div>
<h1 style="position:absolute;left:80px;top:150px;font-size:100px;line-height:1.32">あなたの<span class="mk">1本</span>を、<br>見つけよう。</h1>
<div style="position:absolute;left:0;right:0;top:470px;height:420px;overflow:visible">{fan}</div>
<div style="position:absolute;left:80px;right:80px;top:950px;font-size:36px;line-height:1.6;font-weight:700">
  色も、形も、打ち心地も、いろいろ。<br>握り比べて、好きなデザインで選んでもいい。</div>
<div style="position:absolute;left:80px;right:80px;top:1095px;font-size:27px;color:#444">体験会やレンタルのあるコートは、プロフィールのリンクから</div>
<div class="note" style="position:absolute;left:80px;top:1195px;font-size:21px">画像：各メーカー</div>\n<div class="en" style="position:absolute;right:80px;top:1190px;font-size:26px;color:{GRAY}">NEXT : FILE 02</div>
"""))

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i, html in enumerate(slides, 1):
        f = os.path.abspath(f"{OUT}/s{i}.html")
        open(f, "w").write(html)
        pg.goto("file://" + f)
        pg.wait_for_timeout(300)
        pg.screenshot(path=f"{OUT}/s{i}.png")
    b.close()
print("ok")
