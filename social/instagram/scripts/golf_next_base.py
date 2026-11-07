"""投稿15「ゴルフの次は、ピックルボール？」第3版 1080x1350 × 6枚
python3 post15v3.py 出力先 [ページ...]   （src/ に写真、同じフォルダに Anton.ttf）
"""
import sys, base64, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
def b64(p): return base64.b64encode((HERE / p).read_bytes()).decode()
def img(p): return f"data:image/{'png' if p.endswith('png') else 'jpeg'};base64,{b64(p)}"

NAVY, LIME, CREAM = "#0B1626", "#D4F25A", "#F4EEE3"
N = 6
CSS = f"""
@font-face {{ font-family: Anton; src: url(data:font/ttf;base64,{b64('Anton.ttf')}); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:1080px; height:1350px; overflow:hidden; font-family:'Noto Sans CJK JP','Noto Sans JP',sans-serif; }}
.page {{ position:relative; width:1080px; height:1350px; overflow:hidden; }}
.en {{ font-family:Anton; letter-spacing:3px; }}
.b {{ font-weight:900; }}
.foot {{ position:absolute; left:72px; right:72px; bottom:44px; display:flex; justify-content:space-between;
  font-family:Anton; font-size:26px; letter-spacing:3px; opacity:.7; }}
.credit {{ position:absolute; right:24px; padding:6px 16px; border-radius:999px; background:rgba(0,0,0,.55);
  color:#fff; font-size:22px; font-weight:700; }}
.kick {{ font-family:Anton; font-size:40px; letter-spacing:4px; color:{LIME}; }}
.src {{ font-size:24px; opacity:.6; }}
"""

def foot(n, c=CREAM):
    return f'<div class="foot" style="color:{c}"><span>PICKLEBALL TOKYO</span><span>{n}/{N}　@PICKLEBALLTOKYO</span></div>'

def cover():
    return f"""<div class="page" style="background:{NAVY}">
  <img src="{img('src/sp_cover.jpg')}" style="position:absolute;left:0;top:0;width:1080px;height:820px">
  <div style="position:absolute;left:0;top:0;width:1080px;height:820px;background:linear-gradient(180deg,rgba(11,22,38,.7) 0%,rgba(11,22,38,0) 18%,rgba(11,22,38,0) 64%,{NAVY} 100%)"></div>
  <div style="position:absolute;left:72px;top:64px;text-shadow:0 2px 12px rgba(0,0,0,.6)" class="kick">AFTER WORK IN THE USA</div>
  <div class="credit" style="top:64px">写真：Sip &amp; Pickle（マイアミ）</div>
  <div style="position:absolute;left:72px;right:72px;top:790px;color:#fff">
    <div class="b" style="font-size:92px;line-height:1.2">ゴルフの次は、</div>
    <div class="b" style="font-size:112px;line-height:1.2;color:{LIME}">ピックルボール？</div>
    <div style="font-size:40px;font-weight:700;margin-top:26px;opacity:.9">アメリカの大人の、新しい付き合い方</div>
  </div>
  {foot(1)}
</div>"""

def compare():
    card = lambda bg, fg, ac, en, t, money: f"""<div style="width:450px;height:430px;border-radius:32px;background:{bg};color:{fg};padding:38px 40px">
      <div class="en" style="font-size:42px;color:{ac}">{en}</div>
      <div style="font-size:26px;font-weight:700;margin-top:26px;opacity:.7">かかる時間</div>
      <div class="b" style="font-size:100px;line-height:1.15">{t}</div>
      <div style="font-size:26px;font-weight:700;margin-top:24px;opacity:.7">もてなす費用</div>
      <div class="en" style="font-size:64px;line-height:1.2;color:{ac};white-space:nowrap;letter-spacing:1px">{money}</div></div>"""
    return f"""<div class="page" style="background:{CREAM};color:{NAVY};padding:110px 72px 0">
  <div class="kick" style="color:{NAVY};opacity:.55">GOLF VS PICKLEBALL</div>
  <div class="b" style="font-size:66px;line-height:1.3;margin-top:16px">接待ゴルフと、くらべると。</div>
  <div style="display:flex;gap:36px;margin-top:48px">
    {card('#E2DACB', NAVY, '#6B7280', 'GOLF', '半日', '$600〜700')}
    {card(NAVY, '#fff', LIME, 'PICKLEBALL', '2時間', '$80')}
  </div>
  <div class="src" style="margin-top:16px">シカゴの不動産ブローカーの話（Bloomberg、2024年7月）</div>
  <div style="margin-top:60px;padding-left:28px;border-left:10px solid #E2553A">
    <div class="b" style="font-size:44px;line-height:1.55">「ピックルボールは今や、ゴルフと並ぶ<br>“企業アメリカの取引・交流の場”に<br>なりつつある」</div>
    <div style="font-size:28px;font-weight:700;margin-top:12px;opacity:.65">Bloomberg（2024年7月）の記事より</div>
  </div>
  {foot(2, NAVY)}
</div>"""

def growth():
    base, before, after = 1100, 120, 600          # ちょうど5倍
    lx, rx, w = 170, 650, 260
    l_top, r_top = base - before, base - after
    x1, y1 = lx + w, l_top                        # 左の棒の右上の角
    x2, y2 = rx, r_top                            # 右の棒の左上の角（矢じりの先がぴったり届く）
    cx, cy = (x1 + x2) / 2 - 30, (y1 + y2) / 2 - 40   # ゆるいカーブ
    bar = lambda x, h, bg: f'<div style="position:absolute;left:{x}px;top:{base-h}px;width:{w}px;height:{h}px;background:{bg};border-radius:6px 6px 0 0"></div>'
    arrow = f"""<svg style="position:absolute;left:0;top:0" width="1080" height="1350">
      <defs><marker id="h" markerWidth="5" markerHeight="5" refX="5" refY="2.5" orient="auto"><path d="M0,0 L5,2.5 L0,5 Z" fill="{LIME}" stroke="{NAVY}" stroke-width="0.35" stroke-linejoin="round"/></marker></defs>
      <path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{LIME}" stroke-width="10" stroke-linecap="butt" marker-end="url(#h)"/>
    </svg>"""
    return f"""<div class="page" style="background:{NAVY};color:{CREAM};padding:110px 72px 0">
  <div class="kick">NEW YORK</div>
  <div class="b" style="font-size:60px;line-height:1.4;margin-top:20px;color:#fff">ニューヨークのクラブに、<br>会社からの予約の問い合わせが</div>
  {bar(lx, before, '#3A4A63')}
  {bar(rx, after, LIME)}
  {arrow}
  <div style="position:absolute;left:120px;top:520px;color:{LIME};display:flex;align-items:baseline;white-space:nowrap">
    <span class="en" style="font-size:200px;line-height:1;letter-spacing:0">5</span>
    <span class="b" style="font-size:70px;margin-left:10px">倍以上に</span>
  </div>
  <div class="b" style="position:absolute;left:120px;top:735px;color:{LIME};font-size:70px;white-space:nowrap">増えてる</div>
  <div style="position:absolute;left:72px;right:72px;top:{base}px;height:6px;background:{CREAM};opacity:.5"></div>
  <div class="en" style="position:absolute;left:{lx}px;width:{w}px;top:{base+18}px;text-align:center;font-size:48px;color:{CREAM};opacity:.6">BEFORE</div>
  <div class="en" style="position:absolute;left:{rx}px;width:{w}px;top:{base+18}px;text-align:center;font-size:48px;color:{LIME}">AFTER</div>
  <div class="src" style="position:absolute;right:72px;top:{base+100}px">前の年とくらべて（Bloomberg、2024年7月）</div>
  {foot(3)}
</div>"""

def cnp():
    return f"""<div class="page" style="background:{NAVY}">
  <img src="{img('src/cnp_aerial.png')}" style="position:absolute;left:0;top:0;width:1080px;height:720px;object-fit:cover;object-position:50% 60%">
  <div style="position:absolute;left:0;top:620px;width:1080px;height:100px;background:linear-gradient(180deg,rgba(11,22,38,0),{NAVY})"></div>
  <div class="credit" style="top:24px">写真：Chicken N Pickle（ウィチタ店）</div>
  <div style="position:absolute;left:72px;right:72px;top:748px;color:{CREAM}">
    <div style="display:flex;align-items:baseline;gap:22px;white-space:nowrap">
      <span class="en" style="font-size:76px;line-height:1.1;color:{LIME};letter-spacing:2px">CHICKEN N PICKLE</span>
      <span style="font-size:30px;font-weight:700;opacity:.8">カンザスシティ発</span>
    </div>
    <div class="b" style="font-size:58px;line-height:1.35;margin-top:24px;color:#fff">仕事のあとは、飲みながら。</div>
    <div style="font-size:36px;line-height:1.65;margin-top:22px;opacity:.88">コートの横に、チキン料理の店とバー。<br>2016年に1店目、2024年5月には10店に。</div>
  </div>
  {foot(4)}
</div>"""

def sip():
    tile = lambda src, x, label: f"""<div style="position:absolute;left:{x}px;top:900px;width:456px;height:290px;border-radius:24px;overflow:hidden">
      <img src="{img(src)}" style="width:456px;height:290px;object-fit:cover">
      <div style="position:absolute;left:16px;bottom:14px;padding:6px 16px;border-radius:999px;background:{NAVY};color:{LIME};font-size:24px;font-weight:700">{label}</div></div>"""
    return f"""<div class="page" style="background:{NAVY}">
  <img src="{img('src/sp_courts.jpg')}" style="position:absolute;left:0;top:0;width:1080px;height:600px;object-fit:cover;object-position:50% 45%">
  <div style="position:absolute;left:0;top:500px;width:1080px;height:100px;background:linear-gradient(180deg,rgba(11,22,38,0),{NAVY})"></div>
  <div class="credit" style="top:24px">写真：Sip &amp; Pickle</div>
  <div style="position:absolute;left:72px;right:72px;top:620px;color:{CREAM}">
    <div style="display:flex;align-items:baseline;gap:22px;white-space:nowrap">
      <span class="en" style="font-size:76px;line-height:1.1;color:{LIME};letter-spacing:2px">SIP &amp; PICKLE</span>
      <span style="font-size:30px;font-weight:700;opacity:.8">マイアミ</span>
    </div>
    <div class="b" style="font-size:58px;line-height:1.35;margin-top:20px;color:#fff">打って、食べて、飲む社交クラブ。</div>
  </div>
  {tile('src/sp_gate.jpg', 72, 'PLAY・EAT・SIP・PARTY')}
  {tile('src/sp_tent.png', 552, '夜のラウンジ')}
  {foot(5)}
</div>"""

def last():
    return f"""<div class="page" style="background:{NAVY};color:{CREAM};padding:150px 72px 0">
  <div class="kick">TOKYO</div>
  <div class="b" style="font-size:96px;line-height:1.3;margin-top:20px;color:#fff">東京なら、<br><span style="color:{LIME};font-size:116px">仕事帰りに。</span></div>
  <div style="font-size:46px;font-weight:700;line-height:1.6;margin-top:44px">次の飲み会、<br>まずはコートで集合してみる？</div>
  <div style="margin-top:72px;background:{LIME};color:{NAVY};border-radius:28px;padding:40px 44px">
    <div style="font-size:38px;font-weight:700;line-height:1.5">駅近のコートは、<br>プロフィールのリンクから</div>
    <div class="en" style="font-size:66px;margin-top:8px;letter-spacing:2px">pickleball-tokyo.com</div>
  </div>
  {foot(6)}
</div>"""

PAGES = {1: cover, 2: compare, 3: growth, 4: cnp, 5: sip, 6: last}

def main():
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "out"); out.mkdir(exist_ok=True)
    pages = [int(a) for a in sys.argv[2:]] or list(PAGES)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i in pages:
            pg.set_content(f"<style>{CSS}</style>{PAGES[i]()}"); pg.wait_for_timeout(400)
            pg.screenshot(path=str(out / f"p15_{i}.png"))
        b.close()

if __name__ == "__main__":
    main()
