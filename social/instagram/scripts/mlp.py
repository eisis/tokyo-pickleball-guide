import sys, pathlib, base64
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
def b64(p):
    mime = "font/woff2" if p.endswith("woff2") else "image/png"
    return f"data:{mime};base64," + base64.b64encode((D / p).read_bytes()).decode()
FONT = b64("package/files/anton-latin-400-normal.woff2")
I = {k: b64(f"{k}.png") for k in ["cover2","photo","mlplogo","logos","finals_logo","finals_court","lg_fives","celebrate","pt_icon","tt_court","champs_top"]+[f"ev_{e}" for e in ["dal","col","stl","aus","stp","nyc","sd","chi","orl","pdal","pnb","fin"]]}
OR, NV, PANEL, GR, LT = "#F06B3C", "#0C1830", "#16284A", "#9AA6BC", "#D5DBE6"
N = 7
CR = "画像：Major League Pickleball"

CSS = f"""
@font-face {{ font-family: Anton; src: url('{FONT}') format('woff2'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; background:{NV}; color:#fff; font-family:'Noto Sans CJK JP'; position:relative; overflow:hidden; }}
.a {{ position:absolute; }}
.tag {{ left:72px; top:64px; display:flex; align-items:center; gap:18px; font-family:Anton; font-size:30px; letter-spacing:4px; }}
.tag .bar {{ width:44px; height:8px; background:{OR}; }}
.tag .no {{ color:{GR}; }}
.foot {{ right:72px; bottom:40px; font-family:Anton; font-size:26px; letter-spacing:3px; color:{GR}; }}
.h {{ left:72px; right:72px; font-size:96px; font-weight:900; line-height:1.22; letter-spacing:-1px; }}
.sub {{ left:72px; right:72px; font-size:42px; color:{LT}; }}
.o {{ color:{OR}; }}
.big {{ font-family:Anton; color:{OR}; line-height:1; }}
.credit {{ left:72px; font-size:22px; color:{GR}; }}
"""
def tag(): return '<div class="a tag"><span class="bar"></span>SPECIAL FEATURE<span class="no">｜MLP</span></div>'
def foot(n): return f'<div class="a foot">{n}/{N} @PICKLEBALLTOKYO</div>'
def credit(t, top=1236): return f'<div class="a credit" style="top:{top}px;">{t}</div>'
def fade(top, h, src, pos="center"):
    return f"""<div class="a" style="left:0;right:0;top:{top}px;height:{h}px;background:url({src}) {pos}/cover;"></div>
<div class="a" style="left:0;right:0;top:{top}px;height:{h}px;background:linear-gradient(180deg,{NV} 0%,rgba(12,24,48,0) 18%,rgba(12,24,48,0) 70%,{NV} 100%);"></div>"""
S = {}

S[1] = f"""
<div class="a" style="left:0;right:0;top:130px;height:700px;background:url({I['champs_top']}) center top/cover;"></div>
<div class="a" style="left:0;right:0;top:130px;height:700px;background:linear-gradient(180deg,{NV} 0%,rgba(12,24,48,0) 9%,rgba(12,24,48,0) 66%,{NV} 98%);"></div>
<div class="a" style="left:0;top:120px;width:300px;height:130px;background:radial-gradient(ellipse 100% 100% at 30% 20%,{NV} 55%,rgba(12,24,48,0) 100%);"></div>
{tag()}
<div class="a" style="left:72px;top:770px;display:flex;align-items:center;gap:22px;">
  <img src="{I['mlplogo']}" style="height:64px;border-radius:8px;display:block;">
  <span style="font-family:Anton;font-size:46px;letter-spacing:3px;color:{OR};">MAJOR LEAGUE PICKLEBALL</span></div>
<div class="a h" style="top:856px;font-size:94px;">ピックルボールにも、<br><span class="o">メジャーリーグ</span>が<br>ある。</div>
<div class="a" style="left:72px;top:1210px;font-size:36px;color:{LT};">全米20チームが、頂点を争うプロリーグ。</div>
{credit("画像：Major League Pickleball", 1268)}
{foot(1)}"""

S[2] = f"""{tag()}
<div class="a h" style="top:170px;">住んでいる街に、<br><span class="o">推しチーム</span>がある。</div>
<div class="a sub" style="top:450px;">全米<span class="o" style="font-weight:900;">20チーム</span>。各チーム6人、男女混合で戦う。</div>
<div class="a" style="left:72px;right:72px;top:540px;height:640px;border-radius:20px;overflow:hidden;background:#13284F;display:flex;align-items:center;">
  <img src="{I['logos']}" style="width:100%;display:block;"></div>
{credit(CR, 1206)}
{foot(2)}"""

def ev(k, h): return f'<img src="{I["ev_"+k]}" style="height:{h}px;display:block;filter:drop-shadow(0 4px 10px rgba(0,0,0,.45));">'
def stage(top, h, hi, en, jp, when, note, badges):
    return f"""<div class="a" style="left:72px;right:72px;top:{top}px;height:{h}px;border-radius:20px;background:{OR if hi else PANEL};display:flex;align-items:center;padding:0 34px;gap:24px;">
<div style="width:300px;flex:none;"><div style="font-family:Anton;font-size:28px;letter-spacing:2px;color:{'#fff' if hi else OR};">{en}</div>
<div style="font-size:42px;font-weight:900;line-height:1.25;">{jp}</div>
<div style="font-family:Anton;font-size:26px;color:{'#fff' if hi else LT};margin-top:4px;">{when}</div>
<div style="font-size:22px;color:{'#fff' if hi else GR};margin-top:4px;line-height:1.4;">{note}</div></div>
<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;">{badges}</div></div>"""
def up(top): return f'<div class="a" style="left:50%;transform:translateX(-50%);top:{top}px;width:0;height:0;border-left:22px solid transparent;border-right:22px solid transparent;border-bottom:22px solid {OR};"></div>'
row = lambda ks, h: '<div style="display:flex;gap:14px;justify-content:center;">'+''.join(ev(k,h) for k in ks)+'</div>'
S[3] = f"""{tag()}
<div class="a h" style="top:146px;font-size:84px;">優勝まで、<br><span class="o">3つのステージ</span>。</div>
{stage(372,236,True,"FINALS","決勝","AUG 28–30","ニューヨークに<br>4チーム、優勝は1つ",row(["fin"],180))}
{up(620)}
{stage(654,216,False,"PLAYOFFS","プレーオフ","AUG","上位12チームの<br>勝ち抜き戦",row(["pdal","pnb"],170))}
{up(882)}
{stage(916,296,False,"REGULAR SEASON","リーグ戦","MAY – JUL","全米9都市を回って<br>勝ち点を集める",row(["dal","col","stl","aus","stp"],128)+row(["nyc","sd","chi","orl"],128))}
{credit("2026年シーズン　画像・出典：Major League Pickleball", 1230)}
{foot(3)}"""

S[4] = f"""{tag()}
<div class="a h" style="top:170px;">決勝の舞台は、<br><span class="o">セントラルパーク</span>。</div>
<div class="a sub" style="top:430px;">ニューヨークのど真ん中に、満員の客席。</div>
<div class="a" style="left:0;right:0;top:530px;height:640px;background:url({I['photo']}) center 60%/cover;"></div>
<div class="a" style="left:0;right:0;top:530px;height:640px;background:linear-gradient(180deg,{NV} 0%,rgba(12,24,48,0) 14%,rgba(12,24,48,0) 78%,{NV} 100%);"></div>
<div class="a" style="right:60px;top:560px;width:170px;filter:drop-shadow(0 8px 20px rgba(0,0,0,.6));"><img src="{I['finals_logo']}" style="width:100%;display:block;border-radius:10px;"></div>
{credit("画像：Major League Pickleball、St. Louis Shock", 1206)}
{foot(4)}"""

def stat(top, n, unit, label, note):
    return f"""<div class="a" style="left:72px;right:72px;top:{top}px;height:240px;border-radius:20px;background:{PANEL};display:flex;align-items:center;gap:24px;padding:0 40px;">
<div style="width:440px;display:flex;align-items:flex-end;gap:6px;flex:none;"><span class="big" style="font-size:140px;">{n}</span><span style="font-size:46px;font-weight:900;margin-bottom:14px;">{unit}</span></div>
<div><div style="font-size:38px;font-weight:900;line-height:1.3;">{label}</div><div style="font-size:24px;color:{GR};margin-top:8px;line-height:1.4;">{note}</div></div></div>"""
S[5] = f"""{tag()}
<div class="a h" style="top:150px;font-size:88px;">数字で見る、<br><span class="o">決勝の熱狂</span>。</div>
{stat(410,"77","万人","テレビで見た人","全米ネットCBSの平均<br>MLP史上最多")}
{stat(674,"1","万人超","会場に来た人","決勝の3日間で<br>MLPの大会で史上最多")}
{stat(938,"1,500","万ドル","年間の賞金総額","PPAツアーとMLPの<br>合計（UPA発表）")}
{credit("出典：pickleball.com（2026年8月、2025年6月）", 1206)}
{foot(5)}"""

S[6] = f"""{tag()}
<div class="a h" style="top:150px;font-size:88px;">2026年の王者は、<br><span class="o">3度目の正直</span>。</div>
<div class="a" style="left:0;right:0;top:390px;height:560px;background:url({I['celebrate']}) 45% center/cover;"></div>
<div class="a" style="left:0;right:0;top:390px;height:560px;background:linear-gradient(180deg,{NV} 0%,rgba(12,24,48,0) 12%,rgba(12,24,48,0) 75%,{NV} 100%);"></div>
<div class="a" style="left:72px;right:72px;top:930px;display:flex;align-items:center;gap:28px;">
  <img src="{I['lg_fives']}" style="width:190px;height:155px;object-fit:cover;border-radius:14px;border:3px solid {OR};">
  <div><div style="font-family:Anton;font-size:30px;letter-spacing:3px;color:{OR};">2026 MLP CHAMPION</div>
  <div style="font-size:48px;font-weight:900;">ニュージャージー・ファイブス</div></div></div>
<div class="a sub" style="top:1110px;font-size:36px;line-height:1.5;">2年続けて決勝で敗れたチームが、<span class="o" style="font-weight:900;">ついに初優勝。</span></div>
{credit("出典：pickleball.com／画像：Major League Pickleball", 1250)}
{foot(6)}"""

S[7] = f"""
<div class="a" style="left:0;right:0;top:0;height:900px;background:url({I['tt_court']}) center 70%/cover;"></div>
<div class="a" style="left:0;right:0;top:0;height:900px;background:linear-gradient(180deg,rgba(12,24,48,.97) 0%,rgba(12,24,48,.75) 11%,rgba(12,24,48,0) 26%,rgba(12,24,48,0) 40%,rgba(12,24,48,.75) 72%,{NV} 100%);"></div>
{tag()}
<div class="a" style="right:72px;top:56px;background:rgba(12,24,48,.75);border:2px solid rgba(255,255,255,.35);border-radius:999px;padding:8px 22px;font-size:24px;font-weight:700;">📍 東京タワーのコート</div>
<div class="a" style="left:72px;right:72px;top:620px;font-size:52px;font-weight:900;">推しチームを見つけたら、</div>
<div class="a" style="left:72px;right:72px;top:696px;font-size:104px;font-weight:900;line-height:1.15;color:{OR};">自分でも<br>打ってみよう。</div>
<div class="a" style="left:72px;right:72px;top:960px;height:250px;border-radius:24px;background:{PANEL};border:2px solid #2C4270;display:flex;align-items:center;gap:36px;padding:0 40px;">
  <img src="{I['pt_icon']}" style="width:170px;height:170px;border-radius:36px;flex:none;box-shadow:0 8px 24px rgba(0,0,0,.4);">
  <div><div style="font-size:50px;font-weight:900;letter-spacing:-.5px;">Pickleball <span style="color:#E3F53A;">Tokyo</span></div>
  <div style="font-size:28px;color:{LT};margin-top:6px;">体験会・練習会・コートを、まとめて探せる</div>
  <div style="font-family:Anton;font-size:40px;letter-spacing:2px;color:{OR};margin-top:10px;">PICKLEBALL-TOKYO.COM</div></div></div>
<div class="a" style="left:72px;top:1236px;font-size:26px;color:{GR};">プロフィールのリンクから →</div>
{foot(7)}"""

out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
only = [int(x) for x in sys.argv[2:]]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1350})
    for n, body in S.items():
        if only and n not in only: continue
        pg.set_content(f"<html><head><style>{CSS}</style></head><body>{body}</body></html>")
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        pg.screenshot(path=str(out / f"mlp_{n:02d}.png"))
    b.close()
