"""投稿12：アンナ・リー・ウォーターズの9年（HTMLで組んでPlaywrightで書き出す）
python3 alw.py 出力先フォルダ [ページ番号...]
"""
import sys, os, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
ANTON = (HERE / "fonts" / "Anton.ttf").as_uri()
OUT = HERE / "out"
PA = (OUT / "photo_a.jpg").as_uri(); PB = (OUT / "photo_b.jpg").as_uri()
N = 8
LIME = "#D9FF3D"

CSS = f"""
@font-face {{ font-family: Anton; src: url('{ANTON}'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1350px; }}
body {{ font-family:'Noto Sans CJK JP'; color:#fff; overflow:hidden; position:relative;
  background: radial-gradient(120% 70% at 75% 30%, #15476b 0%, #0b2a45 45%, #050f1c 100%); }}
.grain {{ position:absolute; inset:0; background:
  repeating-linear-gradient(0deg, rgba(255,255,255,.018) 0 2px, transparent 2px 4px); }}
.court {{ position:absolute; inset:0; opacity:.16; }}
.kicker {{ z-index:5; text-shadow:0 2px 12px rgba(0,0,0,.6); position:absolute; left:84px; top:92px; font-family:Anton; font-size:34px; letter-spacing:.18em; color:{LIME}; }}
.kicker span {{ color:#fff; opacity:.8; margin-left:18px; font-family:"Noto Sans CJK JP"; font-weight:700; letter-spacing:.04em; font-size:32px; }}
.giant {{ position:absolute; font-family:Anton; line-height:.8; letter-spacing:-.02em; }}
.outline {{ color:transparent; -webkit-text-stroke:3px rgba(255,255,255,.22); }}
.foot {{ position:absolute; left:84px; right:84px; bottom:58px; display:flex; justify-content:space-between;
  font-family:Anton; font-size:26px; letter-spacing:.16em; color:rgba(255,255,255,.55); }}
.ball {{ position:absolute; border-radius:50%;
  background: radial-gradient(circle at 34% 30%, #ffffff 0 6%, #F2FF9A 14%, {LIME} 45%, #8DB800 100%);
  box-shadow: 0 0 60px 14px rgba(217,255,61,.45), 0 0 160px 40px rgba(217,255,61,.18); }}
.ball i {{ position:absolute; width:13%; height:13%; border-radius:50%; background:rgba(60,80,0,.38); }}
.trail {{ position:absolute; height:22px; border-radius:22px; transform-origin:right center;
  background: linear-gradient(90deg, rgba(217,255,61,0), rgba(217,255,61,.55)); filter: blur(2px); }}
.hang {{ margin-left:-.5em; }}
.photo {{ position:absolute; left:0; width:1080px; }}
.fade {{ position:absolute; left:0; width:1080px; }}
.credit {{ z-index:5; position:absolute; font-size:22px; color:rgba(255,255,255,.6); }}
.h {{ font-size:104px; font-weight:900; line-height:1.2; }}
.b {{ font-size:46px; font-weight:500; line-height:1.55; color:rgba(255,255,255,.82); }}
.lime {{ color:{LIME}; }}
.label {{ display:inline-block; font-family:Anton; font-size:36px; letter-spacing:.14em; color:#06121f;
  background:{LIME}; padding:8px 20px 6px; border-radius:6px; }}
"""

COURT = """<svg class="court" viewBox="0 0 1080 1350" xmlns="http://www.w3.org/2000/svg">
<g fill="none" stroke="#fff" stroke-width="3">
<polygon points="250,820 830,820 1080,1350 0,1350"/>
<line x1="540" y1="820" x2="540" y2="1350"/>
<line x1="170" y1="990" x2="910" y2="990"/>
</g></svg>"""


def ball(x, y, d, trail=0, angle=0):
    holes = "".join(f'<i style="left:{l}%;top:{t}%"></i>' for l, t in
                    [(26, 22), (60, 18), (72, 52), (44, 46), (20, 58), (50, 74), (78, 30)][:7])
    t = ""
    if trail:
        t = (f'<div class="trail" style="left:{x+d/2-trail}px;top:{y+d/2-11}px;width:{trail}px;'
             f'transform:rotate({angle}deg)"></div>')
    return t + f'<div class="ball" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px">{holes}</div>'


def frame(n, body, kicker="THE STORY", sub="ANNA LEIGH WATERS", court=False):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
{COURT if court else ''}<div class="grain"></div>
<div class="kicker">{kicker}<span>{sub}</span></div>
{body}
<div class="foot"><span>PICKLEBALL TOKYO</span><span>{n}/{N}  @PICKLEBALLTOKYO</span></div>
</body></html>"""



def photo(src, top, h, fade_from, fade_to, soft_top=0, pos="center"):
    """写真を置き、下に向かって背景に溶かす（マスク）。上は少し暗くして小見出しを読みやすくする"""
    m = (f"linear-gradient(180deg,{'transparent 0px,' if soft_top else ''}#000 {soft_top}px,#000 {fade_from-top}px,transparent {fade_to-top}px)")
    return (f'<img class="photo" src="{src}" style="top:{top}px;height:{h}px;object-fit:cover;object-position:{pos};'
            f'-webkit-mask-image:{m};mask-image:{m}">' + ('' if soft_top else
            f'<div class="fade" style="top:{top}px;height:240px;background:linear-gradient(180deg,'
            f'rgba(5,15,28,.6),rgba(5,15,28,0))"></div>'))


CHIP = 'display:inline-block;margin:0 12px 0 0;padding:8px 22px;border:2px solid rgba(217,255,61,.7);border-radius:40px;font-size:36px;font-weight:700;background:rgba(7,26,44,.5)'


def p1():
    chips = "".join(f'<span style="{CHIP}">{t}</span>' for t in ["シングルス","ダブルス","混合ダブルス"])
    body = f"""
{photo(PA, 0, 1078, 500, 790)}
<div class="credit" style="right:84px;top:700px">写真：Franklin Sports</div>
<div style="position:absolute;left:84px;top:770px;width:920px">
  <div style="font-size:44px;font-weight:700">アンナ・リー・ウォーターズ<span style="font-weight:500;color:rgba(255,255,255,.75)">（19歳）</span></div>
  <div style="margin-top:20px">{chips}</div>
  <div style="margin-top:22px;font-size:84px;font-weight:900;line-height:1.1">いま、全部</div>
  <div style="font-size:164px;font-weight:900;line-height:1.05" class="lime">世界1位。</div>
</div>
"""
    return frame(1, body, kicker="PICKLEBALL", sub="世界1位の、はじまりの話")


def chapter(n, age, head_html, body_html, pre="", suf="歳", lead=""):
    body = f"""
{ball(860, 430, 100)}
<div style="position:absolute;left:84px;top:{280 if lead else 350}px;width:920px">
  {f'<div style="font-size:44px;font-weight:700;color:rgba(255,255,255,.7);margin-bottom:10px">{lead}</div>' if lead else ''}
  <div><span class="lime" style="font-family:Anton;font-size:230px;line-height:1">{age}</span><span style="font-size:60px;font-weight:900;margin-left:14px">{suf}</span></div>
  {f'<div style="margin-top:22px;font-size:46px;font-weight:700;color:rgba(255,255,255,.75)">{pre}</div>' if pre else ''}
  <div class="h" style="margin-top:{10 if pre else 26}px">{head_html}</div>
  <div class="b" style="margin-top:40px">{body_html}</div>
</div>
"""
    return frame(n, body)


def p2():
    return chapter(2, 8, "テニスは、<br><span class='lime'>大嫌い</span>だった。",
                   "大会に出て、結果も出ていた。<br>なのに、勝っても楽しくなかった。", lead="時計を戻して、", suf="歳")


def p3():
    body = f"""
{ball(860, 430, 100)}
<div style="position:absolute;left:84px;top:350px;width:920px">
  <div><span class="lime" style="font-family:Anton;font-size:230px;line-height:1">10</span><span style="font-size:60px;font-weight:900;margin-left:14px">歳</span></div>
  <div class="b" style="margin-top:26px">ハリケーンで避難した、祖父の家。</div>
  <div class="hang" style="margin-top:20px;font-size:52px;font-weight:700">「ピックルボール、やってみる？」</div>
  <div class="hang" style="margin-top:26px;font-size:104px;font-weight:900;line-height:1.18">「別に、<br><span class="lime" style="margin-left:.5em">やりたくない。」</span></div>
</div>
"""
    return frame(3, body)


def p4():
    return chapter(4, 10, "しぶしぶ1回の<br>はずが、<span class='lime'>夢中。</span>",
                   "そこから2週間、毎日。<br>テニスとちがって、とにかく楽しかった。", suf="歳")


def p5():
    return chapter(5, 12, "母とのペアで、<br>世界トップを<br><span class='lime'>倒す。</span>",
                   "同じ大会で、史上最年少のプロ選手に。<br><span style='font-size:34px;color:rgba(255,255,255,.6)'>ギネス世界記録</span>")


def p6():
    return chapter(6, 16, "3種目ぜんぶ、<br><span class='lime'>世界1位。</span>",
                   "シングルス・ダブルス・混合ダブルス。<br>運転免許を取るより、先に。")


def p7():
    body = f"""
{photo(PB, 150, 645, 480, 725, soft_top=110)}
<div class="credit" style="right:84px;top:660px">写真：Franklin Sports</div>
<div style="position:absolute;left:84px;top:670px;width:920px">
  <div><span class="lime" style="font-family:Anton;font-size:160px;line-height:1">19</span><span style="font-size:52px;font-weight:900;margin-left:14px">歳、いま。</span></div>
  <div style="margin-top:20px;font-size:92px;font-weight:900;line-height:1.2">プロツアーで<br>優勝<span class="lime">200回。</span></div>
  <div class="b" style="margin-top:16px;font-size:40px">TIMEの「スポーツ界の100人」にも。</div>
</div>
"""
    return frame(7, body)


def p8():
    body = f"""
{ball(800, 230, 140, trail=240, angle=-14)}
<div style="position:absolute;left:84px;top:250px;width:920px">
  <div style="font-size:50px;font-weight:700;color:rgba(255,255,255,.75)">始まりは、</div>
  <div class="h" style="margin-top:6px">しぶしぶの<br><span class="lime">1回。</span></div>
  <div style="margin-top:40px;font-size:64px;font-weight:900;line-height:1.3">次の1回は、<br>あなたの番。</div>
</div>
<div style="position:absolute;left:84px;right:84px;top:880px;padding:36px 44px;border-radius:28px;background:rgba(255,255,255,.08);border:2px solid rgba(217,255,61,.6)">
  <div style="font-size:34px;font-weight:700">体験会・練習会は、プロフィールのリンクから</div>
  <div style="margin-top:8px;font-family:Anton;font-size:54px;letter-spacing:.04em" class="lime">PICKLEBALL-TOKYO.COM</div>
</div>
<div style="position:absolute;left:84px;top:1150px;font-size:38px;font-weight:500;color:rgba(255,255,255,.75)">始めたい友達に、送ってみてね</div>
"""
    return frame(8, body)


PAGES = {1: p1, 2: p2, 3: p3, 4: p4, 5: p5, 6: p6, 7: p7, 8: p8}

if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    pages = [int(a) for a in sys.argv[2:]] or sorted(PAGES)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for n in pages:
            f = out / f"p{n}.html"; f.write_text(PAGES[n](), encoding="utf-8")
            pg.goto(f.as_uri()); pg.wait_for_timeout(300)
            pg.screenshot(path=str(out / f"alw_{n}.jpg"), type="jpeg", quality=92)
        b.close()
