"""投稿10 作り直し：動くものだけ濃く、動かないものは薄く。半面を大きく、上に点数。
python3 score2.py 出力先
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import ball as ball3d

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350; N = 8
F = '/usr/share/fonts/opentype/noto/NotoSansCJK-%s.ttc'
def font(w, s): return ImageFont.truetype(F % w, s, index=0)
NAVY = (14, 52, 82); SEA = (31, 127, 184); CORAL = (255, 107, 74); SUN = (255, 214, 120)
WHITE = (255, 255, 255); BG = (250, 247, 241); GREY = (120, 128, 136); LIGHT = (200, 206, 212)
C_SURF = (234, 240, 238); C_LINE = (255, 255, 255); C_KIT = (244, 232, 220); C_EDGE = (214, 222, 220)
ME, FRIEND = CORAL, SEA


def T(d, xy, s, f, c, a='la'): d.text(xy, s, font=f, fill=c, anchor=a)


def rich(d, x, y, segs, f, a='l'):
    tw = sum(d.textlength(s, font=f) for s, _ in segs)
    if a == 'c': x -= tw / 2
    for s, c in segs:
        T(d, (x, y), s, f, c, 'ls'); x += d.textlength(s, font=f)


def footer(d, page, c=NAVY):
    T(d, (70, H - 56), 'PICKLEBALL TOKYO', font('Bold', 26), c, 'ls')
    T(d, (W - 70, H - 56), f'{page}/{N}  @pickleballtokyo', font('Medium', 26), c, 'rs')


def card(im, box, r=32, fill=WHITE):
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    x0, y0, x1, y1 = box
    sd.rounded_rectangle((x0 + 4, y0 + 10, x1 + 4, y1 + 10), radius=r, fill=(14, 52, 82, 28))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(im); d.rounded_rectangle(box, radius=r, fill=fill); return d


def bez(p0, p1, p2, n=80):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]


def arrow(im, p0, ctrl, p2, c, w=14, head=34):
    k = 3; L = Image.new('RGBA', (im.width * k, im.height * k), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    pts = [(x * k, y * k) for x, y in bez(p0, ctrl, p2)]
    d.line(pts[:-6], fill=c, width=w * k, joint='curve')
    (x0, y0), (x1, y1) = pts[-8], pts[-1]; a = math.atan2(y1 - y0, x1 - x0); s = head * k
    d.polygon([(x1 + s * 0.2 * math.cos(a), y1 + s * 0.2 * math.sin(a)),
               (x1 - s * math.cos(a - 0.55), y1 - s * math.sin(a - 0.55)),
               (x1 - s * math.cos(a + 0.55), y1 - s * math.sin(a + 0.55))], fill=c)
    im.alpha_composite(L.resize(im.size, Image.LANCZOS))


def token(im, cx, cy, r, color, name):
    k = 3; S = int(r * 2.8)
    L = Image.new('RGBA', (S * k, S * k), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    c = S * k / 2; R = r * k
    d.ellipse((c - R + 3 * k, c - R + 8 * k, c + R + 3 * k, c + R + 8 * k), fill=(14, 52, 82, 50))
    L = L.filter(ImageFilter.GaussianBlur(5 * k)); d = ImageDraw.Draw(L)
    d.ellipse((c - R * 1.08, c - R * 1.08, c + R * 1.08, c + R * 1.08), fill=WHITE)
    d.ellipse((c - R, c - R, c + R, c + R), fill=color)
    ink = WHITE if color in (SEA, NAVY) else (80, 30, 20); blush = (255, 175, 165)
    for sx in (-1, 1):
        ex, ey = c + sx * R * 0.32, c - R * 0.2
        d.ellipse((ex - R * 0.09, ey - R * 0.12, ex + R * 0.09, ey + R * 0.12), fill=ink)
        d.ellipse((c + sx * R * 0.56 - R * 0.15, c + R * 0.08 - R * 0.09, c + sx * R * 0.56 + R * 0.15, c + R * 0.08 + R * 0.09), fill=blush)
    d.arc((c - R * 0.26, c - R * 0.18, c + R * 0.26, c + R * 0.26), 20, 160, fill=ink, width=int(R * 0.08))
    im.alpha_composite(L.resize((S, S), Image.LANCZOS), (int(cx - S / 2), int(cy - S / 2)))
    d = ImageDraw.Draw(im); f = font('Black', 30)
    tw = d.textlength(name, font=f) + 30
    d.rounded_rectangle((cx - tw / 2, cy + r * 0.45, cx + tw / 2, cy + r * 0.45 + 46), radius=23, fill=WHITE)
    T(d, (cx, cy + r * 0.45 + 23), name, f, color, 'mm')


def put_ball(im, x, y, r=30):
    """すっきりした黄色のボール：白いふち、穴は6つ＋真ん中、下側にうすい陰"""
    k = 4; S = int(r * 3); c = S * k / 2; R = r * k
    L = Image.new('RGBA', (S * k, S * k), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse((c - R * 1.12, c - R * 1.12 + 5 * k, c + R * 1.12, c + R * 1.12 + 5 * k), fill=(14, 52, 82, 55))
    L = L.filter(ImageFilter.GaussianBlur(3 * k)); d = ImageDraw.Draw(L)
    d.ellipse((c - R * 1.13, c - R * 1.13, c + R * 1.13, c + R * 1.13), fill=WHITE)
    d.ellipse((c - R, c - R, c + R, c + R), fill=(250, 196, 20))
    d.ellipse((c - R * 0.97, c - R * 1.0, c + R * 0.9, c + R * 0.86), fill=(255, 214, 40))
    hr = R * 0.13
    for i in range(6):
        a = math.radians(i * 60 + 30)
        hx, hy = c + math.cos(a) * R * 0.56, c + math.sin(a) * R * 0.56
        d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=(238, 168, 0))
    d.ellipse((c - hr, c - hr, c + hr, c + hr), fill=(238, 168, 0))
    im.alpha_composite(L.resize((S, S), Image.LANCZOS), (int(x - S / 2), int(y - S / 2)))


def half(im, x, y, w, h, label=True):
    """自分たちの半面（上がネット）。色は薄く、主役のコマを立たせる"""
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x - 18, y - 18, x + w + 18, y + h + 18), radius=24, fill=C_EDGE)
    d.rectangle((x, y, x + w, y + h), fill=C_SURF)
    kit = h * 7 / 22
    d.rectangle((x, y, x + w, y + kit), fill=C_KIT)
    for ln in [(x, y + kit, x + w, y + kit), (x + w / 2, y + kit, x + w / 2, y + h)]:
        d.line(ln, fill=C_LINE, width=6)
    d.rectangle((x, y, x + w, y + h), outline=C_LINE, width=6)
    d.rectangle((x - 18, y - 6, x + w + 18, y + 6), fill=LIGHT)  # ネット（薄く）
    if label: T(d, (x + w / 2, y - 30), 'ネット', font('Medium', 24), GREY, 'ms')
    ty = y + kit + (h - kit) * 0.50
    fl = font('Black', 30)
    T(d, (x + 22, y + kit + 44), '左', fl, LIGHT, 'ls'); T(d, (x + w - 22, y + kit + 44), '右', fl, LIGHT, 'rs')
    return {'L': (x + w * 0.25, ty), 'R': (x + w * 0.75, ty), 'kit': y + kit}


def side_labels(d, x, y, w):
    T(d, (x + w * 0.25, y), '左', font('Black', 34), GREY, 'ms')
    T(d, (x + w * 0.75, y), '右', font('Black', 34), GREY, 'ms')


def score_head(d, cx, y, num, changed=False):
    c = CORAL if changed else NAVY
    f = font('Black', 88); fs = font('Bold', 40)
    tw = d.textlength(str(num), font=f) + d.textlength('点', font=fs) + 6
    x = cx - tw / 2
    T(d, (x, y), str(num), f, c, 'ls'); T(d, (x + d.textlength(str(num), font=f) + 6, y), '点', fs, c, 'ls')


def tag(d, s, y=66):
    f = font('Bold', 36); tw = d.textlength(s, font=f) + 52
    d.rounded_rectangle((70, y, 70 + tw, y + 62), radius=31, fill=NAVY)
    T(d, (96, y + 31), s, f, WHITE, 'lm')


def bg(c=BG):
    im = Image.new('RGBA', (W, H), c + (255,)); return im, ImageDraw.Draw(im)


def title(d, lines, y=160, size=92):
    f = font('Black', size)
    for i, segs in enumerate(lines):
        rich(d, 70, y + i * int(size * 1.28), segs, f)


def save(im, n): im.convert('RGB').save(os.path.join(OUT, f'score_{n}.png'))


RULES = [('点が入るのは', '自分たちがサーブしているとき', 'だけ', '相手のサーブ中に勝ったら、サーブが回ってくるだけ'),
         ('左右が動くのは', '自分たちのサーブで点を取ったとき', 'だけ', '負けたときは、だれも動かない'),
         ('最初にサーブするのは', '右にいる人', '', 'サーブが回ってきたら、どちらのチームも')]


def rule_cards(im, y0, dark=False, step=282, hh=260):
    for i, (a_, b_, c_, sub) in enumerate(RULES):
        y = y0 + i * step
        fill = (28, 74, 112) if dark else WHITE
        d = card(im, (70, y, W - 70, y + hh), r=30, fill=fill)
        d.ellipse((104, y + 34, 176, y + 106), fill=SUN if dark else NAVY)
        T(d, (140, y + 70), str(i + 1), font('Black', 44), NAVY if dark else WHITE, 'mm')
        T(d, (200, y + 90), a_, font('Black', 50), WHITE if dark else NAVY, 'ls')
        fb = font('Black', 46); hc = SUN if dark else CORAL
        bw = d.textlength(b_, font=fb)
        d.rounded_rectangle((110, y + 162, 110 + bw, y + 180), radius=8, fill=(84, 110, 120) if dark else (255, 214, 196))
        rich(d, 110, y + 166, [(b_, hc), (c_, WHITE if dark else NAVY)], fb)
        T(d, (110, y + 226), sub, font('Medium', 32), (190, 214, 232) if dark else GREY, 'ls')


# ---------- 2 答え：覚えるのは3つだけ ----------
im, d = bg()
title(d, [[('覚えるのは、', NAVY)], [('この3つだけ', CORAL)]], y=150)
rule_cards(im, 360)
footer(ImageDraw.Draw(im), 2); save(im, 2)

# ---------- 4 点を取ったら、左右チェンジ ----------
im, d = bg()
tag(d, '自分たちがサーブしているとき')
title(d, [[('点を取ったら、', NAVY)], [('左右チェンジ', CORAL)]], y=240, size=84)
# 上が「まえ」、下が「あと」。2人の矢印が、まえの位置からあとの位置へ交差する
cx0, cw, ch = 330, 680, 270
ya, yb = 430, 830
r = 50
d = ImageDraw.Draw(im)


def row_label(d, y, word, num, c, bgc):
    f = font('Bold', 34); tw = d.textlength(word, font=f) + 44
    d.rounded_rectangle((70, y, 70 + tw, y + 56), radius=28, fill=bgc)
    T(d, (70 + tw / 2, y + 28), word, f, WHITE, 'mm')
    fn = font('Black', 88)
    T(d, (70, y + 150), str(num), fn, c, 'ls')
    T(d, (70 + d.textlength(str(num), font=fn) + 8, y + 150), '点', font('Bold', 42), c, 'ls')


row_label(d, ya, 'まえ', 0, NAVY, GREY)
row_label(d, yb + 30, 'あと', 1, CORAL, CORAL)
Pa = half(im, cx0, ya, cw, ch, label=True); Pb = half(im, cx0, yb, cw, ch, label=False)
d = ImageDraw.Draw(im)
# まえとあとの間：点を取った！
f = font('Black', 56)
T(d, (66, ya + 240), '点を', f, CORAL, 'ls')
T(d, (66, ya + 306), '取った！', f, CORAL, 'ls')
token(im, *Pa['R'], r, ME, 'あなた'); token(im, *Pa['L'], r, FRIEND, '友達')
put_ball(im, Pa['R'][0] + r * 1.12, Pa['R'][1] - r * 0.78)
token(im, *Pb['L'], r, ME, 'あなた'); token(im, *Pb['R'], r, FRIEND, '友達')
put_ball(im, Pb['L'][0] - r * 1.12, Pb['L'][1] - r * 0.78)
# 交差する矢印（友達を先に、あなたを上に重ねる）
s1 = (Pa['L'][0] + 30, Pa['L'][1] + r + 62); e1 = (Pb['R'][0] - 40, Pb['R'][1] - r - 16)
arrow(im, s1, ((s1[0] + e1[0]) / 2 - 20, (s1[1] + e1[1]) / 2 + 10), e1, FRIEND, w=16, head=38)
s2 = (Pa['R'][0] - 30, Pa['R'][1] + r + 62); e2 = (Pb['L'][0] + 40, Pb['L'][1] - r - 16)
arrow(im, s2, ((s2[0] + e2[0]) / 2 + 20, (s2[1] + e2[1]) / 2 + 10), e2, ME, w=16, head=38)
d = card(im, (70, 1160, W - 70, 1262), r=28)
rich(d, W / 2, 1228, [('あなた', CORAL), ('は左へ、', NAVY), ('友達', SEA), ('は右へ。サーブは同じ人', NAVY)], font('Bold', 40), 'c')
footer(ImageDraw.Draw(im), 4); save(im, 4)


YEL = (232, 168, 0)


def full(im, x, y, w, h):
    """コート全体（薄い色）。自分たちは下、相手は上"""
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((x - 18, y - 18, x + w + 18, y + h + 18), radius=24, fill=C_EDGE)
    d.rectangle((x, y, x + w, y + h), fill=C_SURF)
    ny = y + h / 2; kit = h / 2 * 7 / 22
    d.rectangle((x, ny - kit, x + w, ny + kit), fill=C_KIT)
    for ln in [(x, ny - kit, x + w, ny - kit), (x, ny + kit, x + w, ny + kit), (x + w / 2, y, x + w / 2, ny - kit), (x + w / 2, ny + kit, x + w / 2, y + h)]:
        d.line(ln, fill=C_LINE, width=6)
    d.rectangle((x, y, x + w, y + h), outline=C_LINE, width=6)
    d.rectangle((x - 18, ny - 6, x + w + 18, ny + 6), fill=LIGHT)
    by = ny + kit + (y + h - ny - kit) * 0.5; ty = ny - kit - (ny - kit - y) * 0.5
    fl = font('Black', 28)
    T(d, (x + 20, y + h - 18), '左', fl, LIGHT, 'ls'); T(d, (x + w - 20, y + h - 18), '右', fl, LIGHT, 'rs')
    return {'L': (x + w * 0.25, by), 'R': (x + w * 0.75, by), 'oR': (x + w * 0.25, ty), 'oL': (x + w * 0.75, ty)}


def big_word(d, lines, x, y, c, size=56, gap=64):
    for i, l in enumerate(lines): T(d, (x, y + i * gap), l, font('Black', size), c, 'ls')


# ---------- 1 表紙 ----------
im, d = bg(CORAL)
f = font('Bold', 36)
for i, (s_, bgc, fg) in enumerate([('保存版', WHITE, CORAL), ('ダブルス', NAVY, WHITE)]):
    x0 = 70 + i * 190; tw = d.textlength(s_, font=f) + 52
    d.rounded_rectangle((x0, 80, x0 + tw, 142), radius=31, fill=bgc); T(d, (x0 + tw / 2, 111), s_, f, fg, 'mm')
rich(d, 58, 360, [('「', WHITE), ('0-0-2', NAVY), ('」', WHITE)], font('Black', 190))
T(d, (70, 500), 'って、何の数字？', font('Black', 104), WHITE, 'ls')
T(d, (70, 590), '点数と、立つ場所が絵でわかる', font('Bold', 46), WHITE, 'ls')
card(im, (70, 650, W - 70, 1230), r=40, fill=BG)
P = half(im, 190, 760, 700, 400, label=False)
r = 70
token(im, *P['L'], r, FRIEND, '友達'); token(im, *P['R'], r, ME, 'あなた')
put_ball(im, P['R'][0] + r * 1.1, P['R'][1] - r * 0.8, 38)
footer(ImageDraw.Draw(im), 1, WHITE); save(im, 1)

# ---------- 3 3つの数字 ----------
im, d = bg()
title(d, [[('「0-0-2」', CORAL), ('は、', NAVY)], [('この3つ', NAVY)]])
cols = [(230, '0', CORAL, ['自分たち', 'の点']), (540, '0', NAVY, ['相手', 'の点']), (850, '2', SEA, ['サーブする', '人の番号'])]
for cx, n, c, lab in cols:
    T(d, (cx, 640), n, font('Black', 230), c, 'ms')
for cx in (385, 695):
    d.rounded_rectangle((cx - 22, 535, cx + 22, 555), radius=10, fill=LIGHT)
for cx, n, c, lab in cols:
    d = card(im, (cx - 140, 690, cx + 140, 860), r=28)
    d.rounded_rectangle((cx - 60, 690, cx + 60, 700), radius=5, fill=c)
    T(d, (cx, 765), lab[0], font('Black', 40), c, 'ms'); T(d, (cx, 822), lab[1], font('Bold', 40), NAVY, 'ms')
d = card(im, (70, 920, W - 70, 1240), r=32)
T(d, (110, 1000), 'サーブする人が、', font('Bold', 44), NAVY, 'ls')
rich(d, 110, 1066, [('自分たちの点', CORAL), ('から言います', NAVY)], font('Bold', 44))
d.line((110, 1110, W - 110, 1110), fill=(232, 228, 220), width=3)
rich(d, 110, 1176, [('番号は ', GREY), ('1', SEA), ('か', GREY), ('2', SEA), ('。試合のはじめだけ「2」から', GREY)], font('Bold', 36))
footer(ImageDraw.Draw(im), 3); save(im, 3)

# ---------- 5 負けたら、だれも動かない ----------
im, d = bg()
tag(d, '自分たちがサーブしているとき')
title(d, [[('ラリーに負けたら、', NAVY)], [('だれも動かない', CORAL)]], y=240, size=84)
cx0, cw, ch = 330, 680, 270; ya, yb = 430, 830; r = 50
d = ImageDraw.Draw(im)
row_label(d, ya, 'まえ', 0, NAVY, GREY)
row_label(d, yb + 30, 'あと', 0, NAVY, GREY)
Pa = half(im, cx0, ya, cw, ch, label=True); Pb = half(im, cx0, yb, cw, ch, label=False)
d = ImageDraw.Draw(im)
big_word(d, ['ラリーに', '負けた…'], 66, ya + 240, NAVY, size=52, gap=62)
T(d, (70, yb + 230), '点はそのまま', font('Bold', 32), GREY, 'ls')
for P in (Pa, Pb):
    token(im, *P['R'], r, ME, 'あなた'); token(im, *P['L'], r, FRIEND, '友達')
put_ball(im, Pa['R'][0] + r * 1.12, Pa['R'][1] - r * 0.78)
put_ball(im, Pb['L'][0] + r * 1.12, Pb['L'][1] - r * 0.78)
s1 = (Pa['R'][0] - 20, Pa['R'][1] + r + 62); e1 = (Pb['L'][0] + r * 1.12 + 6, Pb['L'][1] - r * 0.78 - 46)
arrow(im, s1, ((s1[0] + e1[0]) / 2 + 10, (s1[1] + e1[1]) / 2 + 30), e1, YEL, w=14, head=36)
d = card(im, (70, 1160, W - 70, 1262), r=28)
rich(d, W / 2, 1228, [('ボール', YEL), ('だけが友達へ。友達は', NAVY), ('今いる場所', CORAL), ('から', NAVY)], font('Bold', 40), 'c')
footer(ImageDraw.Draw(im), 5); save(im, 5)

# ---------- 6 友達も負けたら、相手のサーブ ----------
im, d = bg()
tag(d, '自分たちがサーブしているとき')
title(d, [[('友達も負けたら、', NAVY)], [('相手のサーブ', CORAL)]], y=240, size=84)
cw, ch = 440, 660; x0 = (W - cw) / 2; y0 = 400
P = full(im, x0, y0, cw, ch); r = 44
d = ImageDraw.Draw(im)
T(d, (x0 - 40, y0 + ch - 10), '自分たち', font('Black', 36), NAVY, 'rs')
d = ImageDraw.Draw(im); hx, hy = P['oR']
d.ellipse((hx - r * 1.55, hy - r * 1.55, hx + r * 1.55, hy + r * 1.55), fill=(255, 222, 212))
d.ellipse((hx - r * 1.55, hy - r * 1.55, hx + r * 1.55, hy + r * 1.55), outline=CORAL, width=7)
token(im, *P['oR'], r, NAVY, '相手'); token(im, *P['oL'], r, NAVY, '相手')
token(im, *P['R'], r, ME, 'あなた'); token(im, *P['L'], r, FRIEND, '友達')
put_ball(im, P['oR'][0] + r * 1.12, P['oR'][1] - r * 0.78, 28)
s1 = (P['L'][0] + r * 1.0, P['L'][1] - r * 1.25); e1 = (P['oR'][0] + r * 1.55, P['oR'][1] + 4)
arrow(im, s1, (s1[0] + 130, (s1[1] + e1[1]) / 2), e1, YEL, w=14, head=36)
d = ImageDraw.Draw(im)
for i, l in enumerate(['相手から', '見て右の', '人から']):
    T(d, (x0 - 36, P['oR'][1] - 50 + i * 44), l, font('Black', 34), CORAL, 'rs')
d = card(im, (70, 1102, W - 70, 1262), r=32, fill=CORAL)
T(d, (W / 2, 1160), 'サーブが回ってきたら、どちらのチームも', font('Bold', 38), WHITE, 'ms')
T(d, (W / 2, 1236), '必ず「右」の人から', font('Black', 64), WHITE, 'ms')
footer(ImageDraw.Draw(im), 6); save(im, 6)

# ---------- 7 迷ったら点を見る ----------
im, d = bg()
title(d, [[('迷ったら、', NAVY)], [('自分たちの点', CORAL), ('を見る', NAVY)]])
cw, ch = 440, 420; y0 = 560; xa, xb = 70, W - 70 - cw; r = 50
for xx, head, nums, me in ((xa, '偶数', '0・2・4…点', 'R'), (xb, '奇数', '1・3・5…点', 'L')):
    d = ImageDraw.Draw(im)
    T(d, (xx + cw / 2, 440), head, font('Black', 72), NAVY, 'ms')
    T(d, (xx + cw / 2, 500), nums, font('Bold', 36), GREY, 'ms')
    P = half(im, xx, y0, cw, ch, label=False)
    fr = 'L' if me == 'R' else 'R'
    token(im, *P[fr], r, FRIEND, '友達'); token(im, *P[me], r, ME, 'あなた')
    d = ImageDraw.Draw(im)
    T(d, (P[me][0], y0 + ch + 70), '右' if me == 'R' else '左', font('Black', 52), CORAL, 'ms')
d = card(im, (70, 1100, W - 70, 1262), r=28)
T(d, (W / 2, 1166), '試合のはじめに右にいた人（あなた）は', font('Bold', 40), NAVY, 'ms')
rich(d, W / 2, 1228, [('偶数なら', NAVY), ('右', CORAL), ('、奇数なら', NAVY), ('左', CORAL), ('にいます', NAVY)], font('Bold', 40), 'c')
footer(ImageDraw.Draw(im), 7); save(im, 7)

# ---------- 8 まとめ ----------
im, d = bg(NAVY)
title(d, [[('覚えるのは、', WHITE), ('この3つだけ', SUN)]], y=150, size=76)
rule_cards(im, 200, dark=True, step=264, hh=246)
d = ImageDraw.Draw(im)
T(d, (W / 2, 1052), '保存して、コートで見返してね', font('Bold', 40), WHITE, 'ms')
d = card(im, (170, 1086, W - 170, 1178), r=46)
T(d, (W / 2, 1116), '体験会・練習会はプロフィールのリンクから', font('Bold', 28), GREY, 'mm')
T(d, (W / 2, 1152), 'pickleball-tokyo.com', font('Black', 36), NAVY, 'mm')
d = ImageDraw.Draw(im)
T(d, (W / 2, 1232), '※サーブしている方だけに点が入る、ふつうの数え方の説明です', font('Medium', 26), (190, 214, 232), 'ms')
footer(d, 8, WHITE); save(im, 8)
print('ok')
