# 投稿7「服装と持ち物」（7枚）
# 文字と人物は easy2.py の部品、服・靴・持ち物は items_svg.py（SVG）で描く
# 使い方：python3 outfit.py 出力先フォルダ
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/ig-outfit'
os.makedirs(OUT, exist_ok=True)
src = open(os.path.join(HERE, 'easy2.py'), encoding='utf-8').read().split('# ---------- 1 表紙')[0]
src = src.replace("sys.path.insert(0, SP)", "").replace("OUT = '/home/claude/ig-easy'; os.makedirs(OUT, exist_ok=True)", "")
# 人物の靴を白いスニーカーに（ここだけ差し替え）
src = src.replace("fy + h * 0.01), h * 0.025, NAVY)", "fy + h * 0.01), h * 0.025, SHOE_C)")
SHOE_C = (238, 241, 244)
exec(src)
import items_svg as I
N = 7
WOOD = (222, 184, 135); WOOD2 = (204, 164, 114)


def put(im, item, width, cx=None, cy=None, bottom=None):
    """SVGの絵を幅 width で、中心(cx,cy) か 下端 bottom に合わせて貼る"""
    g, vw, vh = item
    p = I.render(g, vw, vh, width)
    x = int(cx - p.width / 2)
    y = int(cy - p.height / 2) if bottom is None else int(bottom - p.height)
    im.paste(p, (x, y), p)
    return (x, y, x + p.width, y + p.height)


def shadow(im, cx, y, w, a=34):
    """物の下に、うすい影"""
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.ellipse((cx - w / 2, y - 10, cx + w / 2, y + 10), fill=(14, 52, 82, a))
    sh = sh.filter(ImageFilter.GaussianBlur(6)); im.paste(sh, (0, 0), sh)


def badge(d, x, y, ok, r=26):
    c = KIT if ok else CORAL
    d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    if ok: d.ellipse((x - r * 0.52, y - r * 0.52, x + r * 0.52, y + r * 0.52), outline=WHITE, width=int(r * 0.26))
    else:
        k = r * 0.42; w_ = int(r * 0.26)
        d.line([(x - k, y - k), (x + k, y + k)], fill=WHITE, width=w_); d.line([(x + k, y - k), (x - k, y + k)], fill=WHITE, width=w_)


def label(d, cx, base, text, ok=None, size=40, c=NAVY):
    """中央ぞろえのラベル。ok を渡すと前に○×をつける"""
    f_ = font('Black', size); w = d.textlength(text, font=f_)
    if ok is None:
        T(d, (cx, base), text, f_, c, 'ms'); return
    r = size * 0.62; gap = 14; tot = r * 2 + gap + w; x0 = cx - tot / 2
    badge(d, x0 + r, base - size * 0.36, ok, r)
    T(d, (x0 + r * 2 + gap, base), text, f_, KIT if ok else CORAL, 'ls')


def head(tag, title_lines, body_lines):
    im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
    pill(d, 70, 96, tag, font('Black', 36), CORAL, WHITE)
    y = 186
    for t in title_lines:
        assert d.textlength(t, font=font('Black', TITLE)) < 950, t
        T(d, (64, y), t, font('Black', TITLE), NAVY); y += 120
    y += 14
    for b in body_lines:
        assert d.textlength(b, font=font('Medium', BODY)) < 950, b
        T(d, (70, y), b, font('Medium', BODY), INK); y += LH
    top = y + 34
    d = shadow_card(im, (60, top, 1020, 1230))
    return im, d, top


# ---------- 1 表紙：黄色の背景＋服と持ち物の平置き（グリッドでひと目で分かるように） ----------
im = Image.new('RGB', (W, H), SUN); d = ImageDraw.Draw(im)
x_ = pill(d, 70, 92, '保存版', font('Black', 36), CORAL, WHITE)
pill(d, x_ + 16, 92, 'はじめての人へ', font('Black', 36), NAVY, WHITE)
T(d, (62, 186), '何、着ていく？', font('Black', 122), NAVY)
T(d, (62, 332), '何、持っていく？', font('Black', 122), CORAL)
T(d, (70, 536), 'ピックルボールの服装と持ち物', font('Black', 48), NAVY)
d = shadow_card(im, (60, 640, 1020, 1232), fill=WHITE)
# 上の段：着ていく物（ポロ・スコート・キャップ）と飲み物
row1 = 780
put(im, I.polo(I.NAVY), 210, 190, row1)
put(im, I.skort(), 190, 425, row1 + 8)
put(im, I.cap(), 200, 660, row1 + 6)
put(im, I.bottle(), 88, 892, row1)
# 下の段：靴・タオル・パドルとボール
row2b = 1180
shadow(im, 285, row2b - 2, 340)
put(im, I.sneaker(), 380, 285, bottom=row2b)
put(im, I.towel(), 190, 620, bottom=row2b - 6)
p = paddle(width=112, angle=-16)
im.paste(p, (int(880 - p.width / 2), int(row2b + 12 - p.height)), p)
place_ball(im, 770, row2b - 40, 30, glow=False)
d = ImageDraw.Draw(im); footer(d, 1, NAVY)
im.save(f'{OUT}/01.png')

# ---------- 2 服 ----------
im, d, top = head('服', ['服は、', '動きやすければOK'], ['いつものTシャツやジャージで大丈夫。', '特別なウェアはいりません。'])
fy = 1160
d.rounded_rectangle((100, fy - 30, 980, fy + 34), radius=28, fill=(214, 238, 232))
f = Fig(W, H)
front_person(f, 400, fy, 420, NAVY, WHITE, 'man', pad_side=1, pad_c=SUN, collar=WHITE)
front_person(f, 680, fy, 400, WHITE, NAVY, 'woman', pad_side=-1, pad_c=CORAL, collar=NAVY)
o = f.out(); im.paste(o, (0, 0), o); d = ImageDraw.Draw(im)
pill(d, 540, top + 40, 'いつもの運動着でOK', font('Black', 38), KIT, WHITE, anchor='c')
footer(d, 2); im.save(f'{OUT}/02.png')

# ---------- 3 靴 ----------
im, d, top = head('靴', ['靴は、ふだんの', '運動靴でOK'], ['サンダルや革靴は避けましょう。'])
label(d, 540, top + 82, '運動靴', ok=True, size=44)
shadow(im, 540, top + 392, 420)
put(im, I.sneaker(), 480, 540, bottom=top + 392)
d = ImageDraw.Draw(im)
div = top + 440
d.line([(120, div), (960, div)], fill=(232, 226, 214), width=4)
nb = 1145
put(im, I.flipflop(), 74, 330, bottom=nb)
put(im, I.loafer(), 230, 730, bottom=nb)
d = ImageDraw.Draw(im)
label(d, 330, 1200, 'サンダル', ok=False, size=36)
label(d, 730, 1200, '革靴', ok=False, size=36)
footer(d, 3); im.save(f'{OUT}/03.png')

# ---------- 4 屋内 ----------
im, d, top = head('屋内', ['屋内コートは、', '靴の決まりを確認'], ['室内用の運動靴が必要なところも。', '予約のときに確かめておこう。'])
# 床（カードの下の部分を木の床に）
fl = 1060
flo = Image.new('RGBA', im.size, (0, 0, 0, 0)); fd = ImageDraw.Draw(flo)
fd.rounded_rectangle((60, fl, 1020, 1230), radius=36, fill=WOOD + (255,))
fd.rectangle((60, fl, 1020, fl + 40), fill=WOOD + (255,))
for yy in range(fl + 34, 1226, 34): fd.line([(62, yy), (1018, yy)], fill=WOOD2 + (255,), width=3)
fd.rectangle((60, fl + 70, 1020, fl + 80), fill=(255, 255, 255, 255))
im.paste(flo, (0, 0), flo); d = ImageDraw.Draw(im)
pill(d, 540, top + 40, '室内用の靴に、履きかえ', font('Black', 38), NAVY, WHITE, anchor='c')
sb = fl + 26
put(im, I.sneaker(upper='#FFE4A8', accent=I.CORAL, tab=I.NAVY), 320, 280, bottom=sb)
put(im, I.sneaker(upper='#FFFFFF', accent=I.SEA, tab=I.SUN), 320, 800, bottom=sb)
put(im, I.arrow(I.NAVY), 90, 540, cy=sb - 80)
d = ImageDraw.Draw(im)
label(d, 280, sb - 210, '外ではいてきた靴', size=34, c=GREY)
label(d, 800, sb - 210, '室内用の靴', size=34, c=SEA)
footer(d, 4); im.save(f'{OUT}/04.png')

# ---------- 5 道具 ----------
im, d, top = head('道具', ['パドルは、', '借りられる'], ['借りられるコートが多く、', '施設によっては靴まで借りられます。'])
pill(d, 100, top + 40, 'レンタルOK', font('Black', 36), CORAL, WHITE)
t2 = '手ぶらで行けるところも'; f2 = font('Black', 34)
pill(d, 980 - d.textlength(t2, font=f2) - 44, top + 42, t2, f2, KIT, WHITE, padx=22, pady=12)
base = 1160
p1 = paddle(width=180, angle=-14); p2 = paddle(width=180, angle=14, face=(255, 107, 74), face2=(235, 90, 60), accent=(255, 214, 120))
def vis_bottom(p):  # 透明な余白をのぞいた、絵の下端
    return p.getchannel('A').getbbox()[3]
shadow(im, 315, base - 2, 280)
im.paste(p1, (int(250 - p1.width / 2), base - vis_bottom(p1)), p1)
im.paste(p2, (int(385 - p2.width / 2), base + 4 - vis_bottom(p2)), p2)
shadow(im, 805, base - 2, 320)
put(im, I.sneaker(), 340, 805, bottom=base)
shadow(im, 565, base - 2, 60)
place_ball(im, 565, base - 32, 32, glow=False)
d = ImageDraw.Draw(im)
footer(d, 5); im.save(f'{OUT}/05.png')

# ---------- 6 あると安心 ----------
im, d, top = head('＋α', ['あると安心'], ['飲み物とタオル。', '屋外なら、帽子もあると◎。'])
ib = (top + 1230) / 2 + 120  # 物の下端をそろえる
for cx, item, w_ in ((220, I.bottle(), 140), (540, I.towel(), 270), (860, I.cap(), 270)):
    shadow(im, cx, ib, w_ * 0.9, 26)
    put(im, item, w_, cx, bottom=ib)
d = ImageDraw.Draw(im)
for cx, name in ((220, '飲み物'), (540, 'タオル'), (860, '帽子（屋外）')):
    label(d, cx, ib + 80, name, size=40)
footer(d, 6); im.save(f'{OUT}/06.png')

# ---------- 7 チェックリスト＋CTA ----------
im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
pill(d, 70, 96, '保存しておこう', font('Black', 36), CORAL, WHITE)
T(d, (64, 186), '持ち物', font('Black', TITLE), WHITE)
T(d, (64, 306), 'チェックリスト', font('Black', TITLE), SUN)
d.rounded_rectangle((60, 470, 1020, 990), radius=36, fill=WHITE)
items = ['動きやすい服', '運動靴（屋内は室内用も）', '飲み物', 'タオル', '帽子（屋外）']
y = 520
for s in items:
    d.rounded_rectangle((110, y, 170, y + 60), radius=12, outline=NAVY, width=5)
    d.line([(122, y + 32), (138, y + 48), (162, y + 14)], fill=CORAL, width=9, joint='curve')
    T(d, (200, y + 46), s, font('Black', 46), NAVY, 'ls'); y += 92
T(d, (70, 1070), 'レンタルのあるコートは、', font('Medium', 44), WHITE)
T(d, (70, 1130), 'プロフィールのリンクから', font('Medium', 44), WHITE)
pill(d, 640, 1112, 'pickleball-tokyo.com', font('Black', 30), SUN, NAVY, padx=20, pady=12)
footer(d, 7, WHITE)
im.save(f'{OUT}/07.png')

th = [Image.open(f'{OUT}/0{i}.png').resize((360, 450)) for i in range(1, N + 1)]
sheet = Image.new('RGB', (360 * 4 + 50, 450 * 2 + 30), (200, 200, 200))
for i, t in enumerate(th): sheet.paste(t, (10 + (i % 4) * 370, 10 + (i // 4) * 460))
sheet.save(f'{OUT}/sheet.png')
