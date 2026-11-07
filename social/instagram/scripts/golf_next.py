"""投稿15 第5版：Sip & Pickle を外し、4=Chicken N Pickle（飲みながら）、5=なぜ合う？ に組み直す
python3 golf_next.py 出力先
"""
import sys
import golf_next_base as v
from golf_next_base import img, foot, NAVY, LIME, CREAM

def cnp():
    return f"""<div class="page" style="background:{NAVY}">
  <img src="{img('src/cnp_aerial.png')}" style="position:absolute;left:0;top:0;width:1080px;height:680px;object-fit:cover;object-position:50% 60%">
  <div style="position:absolute;left:0;top:580px;width:1080px;height:100px;background:linear-gradient(180deg,rgba(11,22,38,0),{NAVY})"></div>
  <div class="credit" style="top:24px">写真：Chicken N Pickle（ウィチタ店）</div>
  <div style="position:absolute;left:72px;right:72px;top:700px;color:{CREAM}">
    <div class="b" style="font-size:40px;line-height:1.4;color:#fff;margin-bottom:14px">アメリカには今、こんなお店も。</div>
    <div style="display:flex;align-items:baseline;gap:22px;white-space:nowrap">
      <span class="en" style="font-size:76px;line-height:1.1;color:{LIME};letter-spacing:2px">CHICKEN N PICKLE</span>
      <span style="font-size:30px;font-weight:700;opacity:.8">カンザスシティ発</span>
    </div>
    <div class="b" style="font-size:54px;line-height:1.35;margin-top:20px;color:#fff;white-space:nowrap">コートと、レストランとバーが一つに。</div>
    <div style="font-size:36px;line-height:1.65;margin-top:22px;opacity:.88">仕事のあとにそのまま飲めて、<br>会社の懇親会やチームビルディングにも使える。</div>
  </div>
  {foot(4)}
</div>"""

def why():
    row = lambda n, t, sub: f"""<div style="display:flex;align-items:center;gap:36px;height:186px;margin-top:22px;border-radius:28px;background:{NAVY};padding:0 48px">
      <span class="en" style="font-size:84px;color:{LIME};letter-spacing:0;width:96px">{n}</span>
      <div><div class="b" style="font-size:50px;color:#fff;white-space:nowrap">{t}</div>
      <div style="font-size:30px;color:{CREAM};opacity:.8;margin-top:6px;white-space:nowrap">{sub}</div></div></div>"""
    return f"""<div class="page" style="background:{CREAM};color:{NAVY};padding:110px 72px 0">
  <div class="kick" style="color:{NAVY};opacity:.55">WHY PICKLEBALL</div>
  <div class="b" style="font-size:64px;line-height:1.35;margin-top:16px">初心者でも、<br>その日から一緒に楽しめる。</div>
  <div style="margin-top:24px">
    {row('01', 'すぐ始められる', '道具は借りられて、ルールもシンプル')}
    {row('02', '走り回らなくていい', 'コートが小さく、ボールもゆっくり飛ぶ')}
    {row('03', '話しながら打てる', 'ネット際なら、相手まで4メートルほど')}
  </div>
  <div class="b" style="font-size:40px;line-height:1.6;margin-top:40px">上司も、同僚も、はじめての人も、<br>同じコートで、一緒に遊べる。</div>
  {foot(5, NAVY)}
</div>"""

if __name__ == "__main__":
    v.PAGES[4] = cnp
    v.PAGES[5] = why
    sys.argv = [sys.argv[0], sys.argv[1]]
    v.main()
