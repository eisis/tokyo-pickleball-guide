# 投稿7「服装と持ち物」（7枚）
# easy2.py の部品（Fig・front_person など）をそのまま使う
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/ig-outfit'
os.makedirs(OUT, exist_ok=True)
src = open(os.path.join(HERE, 'easy2.py'), encoding='utf-8').read().split('# ---------- 1 表紙')[0]
src = src.replace("sys.path.insert(0, SP)", "").replace("OUT = '/home/claude/ig-easy'; os.makedirs(OUT, exist_ok=True)", "")
exec(src)
N = 7
BROWN = (120, 78, 52); DBROWN = (70, 44, 30); TAN = (214, 170, 120); WOOD = (226, 186, 132); WOOD2 = (206, 162, 108)
LGREY = (225, 228, 232); MGREY = (180, 186, 192)

# ---------- 道具・持ち物の絵（3倍で描いて縮小） ----------
def sneaker(f, x, by, L, upper=CORAL, accent=NAVY, sole=WHITE):
    """右向きのスニーカー。x=かかと、by=靴底の下"""
    u = L / 100
    P = lambda a, b: (x + a * u, by - b * u)
    toe = tuple(min(255, v + 40) for v in upper)
    # 本体（かかと → 履き口 → ベロ → 甲 → つま先）をひとつの形で
    top = bez(P(3, 12), P(0, 40), P(8, 44), n=10) + bez(P(8, 44), P(20, 40), P(30, 40), n=10) \
        + bez(P(30, 40), P(33, 54), P(42, 52), n=10) + bez(P(42, 52), P(66, 42), P(84, 28), n=14) \
        + bez(P(84, 28), P(100, 22), P(99, 12), n=10)
    f.poly(top + [P(3, 12)], upper)
    # つま先（明るい色）
    f.poly(bez(P(80, 30), P(86, 22), P(84, 12), n=8) + [P(99, 12)] + list(reversed(bez(P(84, 28), P(100, 22), P(99, 12), n=10))), toe)
    # かかと
    f.poly(bez(P(3, 12), P(0, 40), P(8, 44), n=10) + [P(15, 42), P(17, 12)], accent)
    # 靴ひも（甲に沿って3本）
    for t in (0.2, 0.45, 0.7):
        cx_, cy_ = 42 + (84 - 42) * t * 0.62, 52 - (52 - 28) * t * 0.62 - 3
        f.limb(P(cx_ - 4, cy_ - 4.5), P(cx_ + 4, cy_ + 3.5), 1.6 * u, 1.6 * u, WHITE)
    # 靴底（厚めのソールと、色の線）
    f.rrect((x, by - 13 * u, x + 101 * u, by), 6 * u, MGREY)
    f.rrect((x + 1.2 * u, by - 11.8 * u, x + 99.8 * u, by - 1.2 * u), 5 * u, sole)
    f.rrect((x + 2 * u, by - 9 * u, x + 99 * u, by - 7 * u), 1 * u, accent)

def sandal(f, x, by, L):
    u = L / 100; P = lambda a, b: (x + a * u, by - b * u)
    f.rrect((x, by - 9 * u, x + 100 * u, by), 4.5 * u, TAN)
    f.rrect((x, by - 4 * u, x + 100 * u, by), 2 * u, BROWN)
    for cx_, w_ in ((38, 18), (70, 16)):
        f.arc((x + (cx_ - w_) * u, by - 34 * u, x + (cx_ + w_) * u, by + 10 * u), 180, 360, BROWN, 6 * u)

def leather(f, x, by, L):
    u = L / 100; P = lambda a, b: (x + a * u, by - b * u)
    body = bez(P(2, 8), P(0, 34), P(8, 36), n=10) + bez(P(8, 36), P(24, 32), P(36, 34), n=10) \
        + bez(P(36, 34), P(70, 30), P(94, 14), n=14) + bez(P(94, 14), P(102, 10), P(98, 6), n=6)
    f.poly(body + [P(98, 6), P(2, 6)], DBROWN)
    f.poly(bez(P(44, 30), P(66, 27), P(84, 18), n=10) + [P(84, 15), P(44, 26)], (110, 74, 52))  # つや
    f.rrect((x, by - 7 * u, x + 100 * u, by), 2.5 * u, (40, 26, 18))
    f.rrect((x + 2 * u, by - 7 * u, x + 22 * u, by + 3 * u), 2 * u, (40, 26, 18))  # ヒール

def bottle(f, x, by, h, body=SEA, cap=NAVY):
    w = h * 0.36
    f.rrect((x - w * 0.32, by - h, x + w * 0.32, by - h * 0.84), h * 0.03, cap)
    f.rrect((x - w * 0.38, by - h * 0.86, x + w * 0.38, by - h * 0.8), h * 0.02, cap)
    f.rrect((x - w / 2, by - h * 0.82, x + w / 2, by), w * 0.3, body)
    f.rrect((x - w / 2, by - h * 0.55, x + w / 2, by - h * 0.32), 0, SUN)
    f.rrect((x - w * 0.34, by - h * 0.76, x - w * 0.22, by - h * 0.6), w * 0.06, (255, 255, 255))

def towel(f, x, by, w, h, c=(168, 214, 236), stripe=WHITE):
    f.rrect((x - w * 0.03, by - h * 0.55, x + w * 1.03, by + h * 0.06), h * 0.14, (140, 196, 224))  # 下に折り重なった部分
    f.rrect((x, by - h, x + w, by), h * 0.12, c)
    for t in (0.12, 0.2):
        f.rrect((x + w * t, by - h, x + w * (t + 0.04), by), 0, stripe)
    for t in (0.76, 0.84):
        f.rrect((x + w * t, by - h, x + w * (t + 0.04), by), 0, stripe)

def cap_side(f, x, by, w, c=NAVY, brim=None):
    """横から見た帽子。クラウンとつばをつなげて描く"""
    brim = brim or tuple(max(0, v - 20) for v in c)
    h = w * 0.5
    f.chord((x, by - h, x + w * 0.72, by + h), 180, 360, c)
    f.poly([(x + w * 0.5, by - h * 0.06), (x + w * 0.72, by - h * 0.12), (x + w * 1.0, by + h * 0.02), (x + w * 0.98, by + h * 0.1), (x + w * 0.5, by + h * 0.06)], brim)
    f.rrect((x - w * 0.01, by - h * 0.1, x + w * 0.62, by + h * 0.06), h * 0.05, brim)
    f.ell((x + w * 0.33, by - h * 1.08, x + w * 0.41, by - h * 0.92), brim)

def polo_flat(f, cx, ty, w, c=SUN, collar=NAVY):
    """平置きのポロシャツ。袖と胴をひとつの形で、なで肩"""
    h = w * 0.95
    sh = bez((cx - w * 0.18, ty), (cx - w * 0.36, ty + h * 0.02), (cx - w * 0.5, ty + h * 0.16), n=10)
    shr = bez((cx + w * 0.5, ty + h * 0.16), (cx + w * 0.36, ty + h * 0.02), (cx + w * 0.18, ty), n=10)
    pts = sh + [(cx - w * 0.42, ty + h * 0.36), (cx - w * 0.3, ty + h * 0.3), (cx - w * 0.3, ty + h), (cx + w * 0.3, ty + h), (cx + w * 0.3, ty + h * 0.3), (cx + w * 0.42, ty + h * 0.36)] + shr
    f.poly(pts, c)
    f.poly([(cx - w * 0.2, ty - h * 0.01), (cx, ty + h * 0.1), (cx - w * 0.06, ty + h * 0.16)], collar)
    f.poly([(cx + w * 0.2, ty - h * 0.01), (cx, ty + h * 0.1), (cx + w * 0.06, ty + h * 0.16)], collar)
    f.rrect((cx - w * 0.025, ty + h * 0.1, cx + w * 0.025, ty + h * 0.3), w * 0.01, tuple(max(0, v - 30) for v in c))
    for t in (0.17, 0.25): f.ell((cx - w * 0.018, ty + h * t - w * 0.018, cx + w * 0.018, ty + h * t + w * 0.018), collar)

def shoebag(f, x, by, w, h, c=NAVY):
    f.poly([(x + w * 0.08, by - h), (x + w * 0.92, by - h), (x + w, by - h * 0.82), (x + w, by), (x, by), (x, by - h * 0.82)], c)
    for t in (0.25, 0.45, 0.65): f.d.line([f.P((x + w * (t - 0.05), by - h)), f.P((x + w * t, by - h * 0.86))], fill=tuple(max(0, v - 20) for v in c), width=int(3 * f.k))
    f.arc((x + w * 0.3, by - h * 1.3, x + w * 0.7, by - h * 0.82), 180, 360, WHITE, h * 0.03)

def badge(d, x, y, ok, r=40):
    c = KIT if ok else CORAL
    d.ellipse((x - r, y - r, x + r, y + r), fill=c, outline=WHITE, width=6)
    if ok: d.ellipse((x - r * 0.5, y - r * 0.5, x + r * 0.5, y + r * 0.5), outline=WHITE, width=int(r * 0.24))
    else:
        k = r * 0.42; w_ = int(r * 0.26)
        d.line([(x - k, y - k), (x + k, y + k)], fill=WHITE, width=w_); d.line([(x + k, y - k), (x - k, y + k)], fill=WHITE, width=w_)

def paste(im, f):
    o = f.out(); im.paste(o, (0, 0), o)
    return ImageDraw.Draw(im)

def head(no, title_lines, body_lines, tag=None):
    im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
    pill(d, 70, 96, tag or no, font('Black', 36), CORAL, WHITE)
    y = 186
    for t in title_lines:
        T(d, (64, y), t, font('Black', TITLE), NAVY); y += 120
    y += 14
    for b in body_lines:
        T(d, (70, y), b, font('Medium', BODY), INK); y += LH
    top = y + 34
    d = shadow_card(im, (60, top, 1020, 1230))
    return im, d, top

# ---------- 1 表紙（ほかの投稿と色を変えて、ひと目で「持ち物」と分かるように） ----------
im = Image.new('RGB', (W, H), SUN); d = ImageDraw.Draw(im)
x_ = pill(d, 70, 92, '保存版', font('Black', 36), CORAL, WHITE)
pill(d, x_ + 18, 92, 'はじめての人へ', font('Black', 36), NAVY, WHITE)
T(d, (62, 186), '何、着ていく？', font('Black', 122), NAVY)
T(d, (62, 332), '何、持っていく？', font('Black', 122), CORAL)
T(d, (70, 532), 'ピックルボールの服装と持ち物', font('Black', 50), NAVY)
d = shadow_card(im, (60, 640, 1020, 1232), fill=WHITE)
f = Fig(W, H)
polo_flat(f, 235, 690, 270, SEA, WHITE)
cap_side(f, 430, 820, 210, CORAL)
bottle(f, 760, 960, 240)
sneaker(f, 100, 1195, 440, CORAL, NAVY)
towel(f, 590, 1190, 190, 90)
d = paste(im, f)
p = paddle(width=130, angle=-24)
im.paste(p, (995 - p.width, 1210 - p.height), p)
place_ball(im, 690, 1035, 38, glow=False)
d = ImageDraw.Draw(im); footer(d, 1, NAVY)
im.save(f'{OUT}/01.png')

# ---------- 2 服 ----------
im, d, top = head('服', ['服は、', '動きやすければOK'], ['いつものTシャツやジャージで大丈夫。', '特別なウェアはいりません。'])
d.rounded_rectangle((90, 1120, 990, 1200), radius=26, fill=(214, 238, 232))
f = Fig(W, H)
front_person(f, 360, 1150, 440, SEA, WHITE, 'man', pad_side=1, pad_c=SUN, collar=WHITE)
front_person(f, 700, 1150, 420, CORAL, NAVY, 'woman', pad_side=-1, pad_c=SUN, collar=WHITE)
d = paste(im, f)
pill(d, 540, top + 40, 'いつもの運動着でOK', font('Black', 40), KIT, WHITE, anchor='c')
footer(d, 2); im.save(f'{OUT}/02.png')

# ---------- 3 靴 ----------
im, d, top = head('靴', ['靴は、ふだんの', '運動靴でOK'], ['サンダルや革靴は避けましょう。'])
f = Fig(W, H)
sneaker(f, 300, top + 420, 560, CORAL, NAVY)
sandal(f, 140, 1120, 300)
leather(f, 620, 1120, 300)
d = paste(im, f)
badge(d, 140, top + 80, True, 40)
T(d, (196, top + 98), '運動靴', font('Black', 46), KIT, 'ls')
d.line([(110, top + 470), (970, top + 470)], fill=(232, 226, 214), width=4)
badge(d, 230, 1180, False, 28); T(d, (272, 1194), 'サンダル', font('Black', 38), CORAL, 'ls')
badge(d, 720, 1180, False, 28); T(d, (762, 1194), '革靴', font('Black', 38), CORAL, 'ls')
footer(d, 3); im.save(f'{OUT}/03.png')

# ---------- 4 屋内 ----------
im, d, top = head('屋内', ['屋内コートは、', '靴の決まりを確認'], ['室内用の運動靴が必要なところも。', '予約のときに確かめておこう。'])
# 体育館の床
fl = top
d.rounded_rectangle((60, fl, 1020, 1230), radius=36, fill=WOOD)
for i, yy in enumerate(range(int(fl) + 40, 1220, 52)):
    d.line([(60, yy), (1020, yy)], fill=WOOD2, width=3)
d.line([(60, 1120), (1020, 1120)], fill=WHITE, width=8)
f = Fig(W, H)
shoebag(f, 130, 1100, 220, 270, NAVY)
sneaker(f, 420, 1100, 500, WHITE, SEA, sole=(245, 245, 245))
d = paste(im, f)
pill(d, 540, top + 50, '室内用の靴に、履きかえ', font('Black', 42), WHITE, NAVY, anchor='c')
footer(d, 4); im.save(f'{OUT}/04.png')

# ---------- 5 道具 ----------
im, d, top = head('道具', ['パドルは、', '借りられる'], ['借りられるコートが多く、', '施設によっては靴まで借りられます。'])
f = Fig(W, H)
sneaker(f, 580, 1185, 380, SUN, NAVY)
d = paste(im, f)
p1 = paddle(width=220, angle=-18); im.paste(p1, (110, top + 130), p1)
p2 = paddle(width=220, angle=16, face=(255, 107, 74), face2=(235, 90, 60), accent=(255, 214, 120)); im.paste(p2, (290, top + 150), p2)
place_ball(im, 720, top + 260, 44, glow=False)
d = ImageDraw.Draw(im)
pill(d, 100, top + 40, 'レンタルOK', font('Black', 38), CORAL, WHITE)
pill(d, 980 - d.textlength('手ぶらで行けるところも', font=font('Black', 34)) - 44, top + 44, '手ぶらで行けるところも', font('Black', 34), KIT, WHITE, padx=22, pady=11)
footer(d, 5); im.save(f'{OUT}/05.png')

# ---------- 6 あると安心 ----------
im, d, top = head('＋α', ['あると安心'], ['飲み物とタオル。', '屋外なら、帽子もあると◎。'])
f = Fig(W, H)
base = 1060
bottle(f, 220, base, 400)
towel(f, 380, base, 300, 160)
cap_side(f, 730, base - 50, 250, NAVY)
d = paste(im, f)
for x, s in ((220, '飲み物'), (530, 'タオル'), (850, '帽子（屋外）')):
    T(d, (x, base + 100), s, font('Black', 40), NAVY, 'ms')
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
