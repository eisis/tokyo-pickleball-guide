# 投稿8「ASICS PICKLEBALL CONNECT（丸の内・東京ビルTOKIA）」8枚
# 事実はすべてASICSの公式発表（2026-10-23）と公式予約ページの画像による
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import os, sys
SCR = '/home/claude/tokyo-pickleball-guide/social/instagram/scripts'
sys.path.insert(0, SCR)
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/ig-asics'
os.makedirs(OUT, exist_ok=True)
src = open(os.path.join(SCR, 'easy2.py'), encoding='utf-8').read().split('# ---------- 1 表紙')[0]
src = src.replace("sys.path.insert(0, SP)", "").replace("OUT = '/home/claude/ig-easy'; os.makedirs(OUT, exist_ok=True)", "")
exec(src)
N = 8
A = '/mnt/user-data/attachments/174b614f-cd49-5a8b-80b9-5950c91298fc/'
COURT = Image.open(A + 'e5db7444-image.jpg').convert('RGB')
SPOT = Image.open(A + 'bcd474e2-image.jpg').convert('RGB')
SPEED = Image.open(A + '5708fe09-image.jpg').convert('RGB')
GAME = Image.open(A + '4ecbbd8d-image.jpg').convert('RGB')
RESO = Image.open(A + '1d06e4a4-image.jpg').convert('RGB')
LAV = (196, 198, 236); VIO = (84, 66, 178); DEEP = (34, 40, 92)   # 会場の色（ラベンダー）に合わせる
CREDIT = '画像：ASICS'
import numpy as np
sys.path.insert(0, SCR)
import items_svg as I


def homog(src, dst):
    A = []
    for (x, y), (u, v) in zip(src, dst):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
    b = [c for pt in dst for c in pt]
    h = np.linalg.solve(np.array(A, float), np.array(b, float))
    Hm = np.append(h, 1).reshape(3, 3)
    def f(x, y):
        X, Y, Z = Hm @ [x, y, 1]
        return (X / Z, Y / Z)
    return f


def court_illust(w, h, k=2):
    """屋内コート2面を斜め上から見たイラスト（公式の画像は使わない）"""
    W2, H2 = w * k, h * k
    im = Image.new('RGB', (W2, H2), (222, 222, 244)); d = ImageDraw.Draw(im)
    # 奥の壁（ガレリアの縦ルーバー）
    wall_y = int(H2 * 0.30)
    d.rectangle((0, 0, W2, wall_y), fill=(176, 178, 222))
    for x in range(0, W2, 26 * k): d.rectangle((x, 0, x + 12 * k, wall_y), fill=(160, 162, 210))
    d.rectangle((0, wall_y - 10 * k, W2, wall_y), fill=(140, 142, 198))
    # 床
    d.rectangle((0, wall_y, W2, H2), fill=(150, 156, 214))
    # 2面分（各 6.1m×13.41m、間 2m）を床の台形に投影。手前を広く
    CW, CL, GAP = 6.1, 13.41, 2.0
    TW = CW * 2 + GAP + 2.0
    src = [(-1.0, 0), (TW - 1.0, 0), (TW - 1.0, CL + 2), (-1.0, CL + 2)]
    dst = [(W2 * 0.20, wall_y + 16 * k), (W2 * 0.80, wall_y + 16 * k), (W2 * 0.99, H2 - 14 * k), (W2 * 0.01, H2 - 14 * k)]
    P = homog([(x, y - 1) for x, y in src], dst)
    poly = lambda pts: [P(x, y) for x, y in pts]
    d.polygon(poly([(-1.0, -1), (TW - 1.0, -1), (TW - 1.0, CL + 1), (-1.0, CL + 1)]), fill=(168, 174, 228))
    for c in range(2):
        x0 = c * (CW + GAP)
        d.polygon(poly([(x0, 0), (x0 + CW, 0), (x0 + CW, CL), (x0, CL)]), fill=(120, 128, 200))
        kz = 2.13
        d.polygon(poly([(x0, CL / 2 - kz), (x0 + CW, CL / 2 - kz), (x0 + CW, CL / 2 + kz), (x0, CL / 2 + kz)]), fill=(104, 112, 186))
        lw = 4 * k
        for a, b in [((x0, 0), (x0 + CW, 0)), ((x0 + CW, 0), (x0 + CW, CL)), ((x0 + CW, CL), (x0, CL)), ((x0, CL), (x0, 0)),
                     ((x0, CL / 2 - kz), (x0 + CW, CL / 2 - kz)), ((x0, CL / 2 + kz), (x0 + CW, CL / 2 + kz)),
                     ((x0 + CW / 2, 0), (x0 + CW / 2, CL / 2 - kz)), ((x0 + CW / 2, CL / 2 + kz), (x0 + CW / 2, CL))]:
            d.line([P(*a), P(*b)], fill=(255, 255, 255), width=lw)
        # ネット（ポールと網）
        l, r = P(x0 - 0.3, CL / 2), P(x0 + CW + 0.3, CL / 2)
        nh = 22 * k * (r[1] / H2 + 0.3)
        d.polygon([l, r, (r[0], r[1] - nh), (l[0], l[1] - nh)], fill=(60, 64, 120))
        for t in range(1, 24):
            x = l[0] + (r[0] - l[0]) * t / 24; yb = l[1] + (r[1] - l[1]) * t / 24
            d.line([(x, yb), (x, yb - nh)], fill=(90, 96, 150), width=k)
        d.line([(l[0], l[1] - nh), (r[0], r[1] - nh)], fill=(255, 255, 255), width=5 * k)
        for q in (l, r): d.rectangle((q[0] - 4 * k, q[1] - nh - 6 * k, q[0] + 4 * k, q[1] + 4 * k), fill=(40, 44, 90))
    return im.resize((w, h), Image.LANCZOS)


def shoe_illust(width, flip=False):
    """ブランドの模様のない、シンプルなシューズのイラスト（斜め上から見た立体）"""
    g, vw, vh = I.sneaker()
    im_ = I.render(g, vw, vh, width)
    return im_.crop(im_.getchannel('A').getbbox())



def trim_white(im, pad=10):
    """白い背景の余白を切り落とす（影は残す）"""
    bg = Image.new('RGB', im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > 18 else 0)
    x0, y0, x1, y1 = diff.getbbox()
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def half(im, side):  # 男女2足の写真を、左右どちらか1足に
    w = im.width
    return trim_white(im.crop((0, 0, w // 2, im.height)) if side == 0 else im.crop((w // 2, 0, w, im.height)))


def knock_white(im):
    """白い背景を透明に（うすい影は半透明で残す）"""
    rgb = im.convert('RGB')
    d_ = ImageChops.difference(rgb, Image.new('RGB', im.size, (255, 255, 255))).convert('L')
    a = d_.point(lambda v: 0 if v < 6 else min(255, int((v - 6) * 6)))
    out = rgb.convert('RGBA'); out.putalpha(a); return out


def pair(img, shoe_h):
    """1モデルの2足（サイトと同じく左・右の順）。左の靴は左下・右の靴は右上に、ほとんど重ねずに並べる。
    靴1足の高さを shoe_h にそろえるので、どのモデルも同じ大きさになる"""
    L = knock_white(fit(half(img, 0), h=shoe_h)); R = knock_white(fit(half(img, 1), h=shoe_h))
    dx = int(L.width * 0.80); dy = int(L.height * 0.36)
    cw = max(L.width, dx + R.width); ch = max(dy + L.height, R.height)
    c = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    c.alpha_composite(R, (dx, 0)); c.alpha_composite(L, (0, dy))  # 手前（左下）の靴をあとに描く
    return c


def paste_c(base, p, cx, cy):
    base.paste(p, (int(cx - p.width / 2), int(cy - p.height / 2)), p)


def fit(im, w=None, h=None):
    if w and h:
        r = min(w / im.width, h / im.height)
    elif w:
        r = w / im.width
    else:
        r = h / im.height
    return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)


def cover_crop(im, w, h, cx=0.5, cy=0.5):
    r = max(w / im.width, h / im.height); im2 = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x = int((im2.width - w) * cx); y = int((im2.height - h) * cy)
    return im2.crop((x, y, x + w, y + h))


def rounded(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=r, fill=255)
    out = im.convert('RGBA'); out.putalpha(m); return out


def photo(base, im, box, r=32, cx=0.5, cy=0.5):
    x0, y0, x1, y1 = box
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x0 + 4, y0 + 12, x1 + 4, y1 + 12), radius=r, fill=(20, 24, 60, 50))
    sh = sh.filter(ImageFilter.GaussianBlur(12)); base.paste(sh, (0, 0), sh)
    p = rounded(cover_crop(im, x1 - x0, y1 - y0, cx, cy), r); base.paste(p, (x0, y0), p)


def credit(d, x, y, text=CREDIT, c=(255, 255, 255), a='rs'):
    T(d, (x, y), text, font('Medium', 22), c, a)


def head(tag, title_lines, body_lines, bg=SAND, tagc=CORAL, tc=NAVY, bc=INK, top_y=96):
    im = Image.new('RGB', (W, H), bg); d = ImageDraw.Draw(im)
    pill(d, 70, top_y, tag, font('Black', 36), tagc, WHITE)
    y = top_y + 90
    for t in title_lines:
        assert d.textlength(t, font=font('Black', TITLE)) < 950, t
        T(d, (64, y), t, font('Black', TITLE), tc); y += 120
    y += 14
    for b in body_lines:
        assert d.textlength(b, font=font('Medium', BODY)) < 950, b
        T(d, (70, y), b, font('Medium', BODY), bc); y += LH
    return im, d, y + 34


def rows(d, x, y, items, kw=210, size=40, gap=86, c=NAVY, kc=GREY, line=(226, 220, 208), x1=1000):
    for k, v in items:
        T(d, (x, y), k, font('Black', 32), kc, 'ls')
        T(d, (x + kw, y), v, font('Black', size), c, 'ls')
        d.line([(x, y + 30), (x1, y + 30)], fill=line, width=3)
        y += gap
    return y


# ---------- 1 表紙：シューズが主役 ----------
im = Image.new('RGB', (W, H), LAV); d = ImageDraw.Draw(im)
x_ = pill(d, 70, 92, '10/31 OPEN', font('Black', 36), CORAL, WHITE)
pill(d, x_ + 16, 92, '12/27までの期間限定', font('Black', 36), DEEP, WHITE)
# 文字の強弱：見出し（92）＞ イベント名（40）。縦の間隔をそろえる
T(d, (68, 230), 'ASICS PICKLEBALL CONNECT', font('Black', 40), DEEP, 'ls')
f92 = font('Black', 96)
T(d, (60, 240), '丸の内に、', f92, DEEP)
# 「ASICS」だけ一回り大きく、紫と下の黄色い線で目立たせる（「の」は見出しと同じ大きさ・同じ高さ）
fA = font('Black', 116); ax = 60 + d.textlength('丸の内に、', font=f92); base = 240 + f92.getmetrics()[0]
aw = d.textlength('ASICS', font=fA)
d.rounded_rectangle((ax + 2, base + 10, ax + aw - 2, base + 22), radius=6, fill=SUN)  # 文字にかからない、下の黄色い線
T(d, (ax, base), 'ASICS', fA, VIO, 'ls')
T(d, (ax + aw + 4, base), 'の', f92, DEEP, 'ls')
T(d, (60, 356), 'ピックルボールコート', f92, DEEP)
ph = (60, 526, 1020, 998)
ci = rounded(court_illust(ph[2] - ph[0], ph[3] - ph[1]), 36); im.paste(ci, (ph[0], ph[1]), ci)
d = ImageDraw.Draw(im)
T(d, (ph[2] - 24, ph[3] - 22), '※イラストはイメージです', font('Medium', 22), WHITE, 'rs')
# シューズの話（写真とは別のカード）。靴と文字のかたまりを、どちらも縦の中央にそろえる
cy0, cy1 = 1052, 1216; mid = (cy0 + cy1) / 2
d.rounded_rectangle((60, cy0, 1020, cy1), radius=32, fill=WHITE)
pc = shoe_illust(230); paste_c(im, pc, 100 + pc.width / 2, mid)
d = ImageDraw.Draw(im)
tx = 92 + pc.width + 32
T(d, (tx, mid - 6), 'ASICSのシューズも借りられる', font('Black', 40), DEEP, 'ls')
f26 = font('Medium', 26); l2 = 'OneASICS会員かASICS公式LINEの追加で'
T(d, (tx, mid + 40), l2, f26, INK, 'ls')
T(d, (tx + d.textlength(l2, font=f26), mid + 40), '無料', font('Black', 26), CORAL, 'ls')
assert tx + d.textlength(l2 + '無料', font=f26) < 995
assert tx + d.textlength('ASICSのシューズも借りられる', font=font('Black', 40)) < 995
T(d, (70, H - 56), 'PICKLEBALL TOKYO', font('Bold', 26), DEEP, 'ls')
T(d, (W - 70, H - 56), f'1/{N}  @pickleballtokyo', font('Medium', 26), DEEP, 'rs')
im.save(f'{OUT}/01.png')

# ---------- 2 場所 ----------
im, d, y = head('場所', ['東京駅から、', '歩いて3分'], ['東京ビルTOKIA 1階のガレリア。', '屋根つきで、天気を気にせずプレーできる。'])
ci = rounded(court_illust(960, 1150 - y), 32); im.paste(ci, (60, y), ci)
d = ImageDraw.Draw(im)
pill(d, 90, y + 26, 'JR東京駅 丸の内南口から徒歩3分', font('Black', 34), WHITE, DEEP, padx=22, pady=12)
T(d, (1000, 1190), '※イラストはイメージです', font('Medium', 24), GREY, 'rs')
footer(d, 2); im.save(f'{OUT}/02.png')

# ---------- 3 コート ----------
im, d, y = head('コート', ['フルサイズ2面、', '毎日7時から22時'], [])
d = shadow_card(im, (60, y, 1020, 1200))
ry = y + 100
rows(d, 110, ry, [('期間', '10/31（土）〜12/27（日）'), ('営業', '毎日 7:00〜22:00'), ('コート', 'フルサイズ 2面'), ('設備', '更衣室あり'), ('場所', '東京ビルTOKIA 1階ガレリア')], kw=200, size=42, gap=106, x1=970)
T(d, (540, ry + 106 * 5 + 30), 'コートの横には、写真を撮れるフォトスポットも。', font('Medium', 34), INK, 'ms')
footer(d, 3); im.save(f'{OUT}/03.png')

# ---------- 4 料金 ----------
im, d, y = head('料金', ['料金は、', '1面1時間で'], ['予約のときに、カードで事前に支払います。'])
d = shadow_card(im, (60, y, 1020, 1230))
ty = y + 90
for k, t, v in (('平日', '7:00〜18:00', '7,000円'), ('平日', '18:00〜22:00', '8,000円'), ('土日祝', '7:00〜22:00', '10,000円')):
    T(d, (110, ty), k, font('Black', 44), NAVY, 'ls'); T(d, (290, ty), t, font('Medium', 40), INK, 'ls')
    T(d, (970, ty), v, font('Black', 52), NAVY, 'rs')
    d.line([(110, ty + 34), (970, ty + 34)], fill=(232, 226, 214), width=3); ty += 104
T(d, (970, ty - 40), '（1面1時間・税込）', font('Medium', 26), GREY, 'rs')
by = ty + 10
d.rounded_rectangle((100, by, 980, by + 170), radius=28, fill=(238, 238, 250))
T(d, (540, by + 62), '4人で割ると', font('Black', 36), DEEP, 'ms')
T(d, (540, by + 134), '1人 1,750円から', font('Black', 60), CORAL, 'ms')
T(d, (540, by + 204), '※平日7〜18時の場合。パドルやシューズのレンタル代は別', font('Medium', 26), GREY, 'ms')
footer(d, 4); im.save(f'{OUT}/04.png')

# ---------- 5 シューズは無料で借りられる（条件つき） ----------
im = Image.new('RGB', (W, H), LAV); d = ImageDraw.Draw(im)
pill(d, 70, 96, 'シューズ', font('Black', 36), CORAL, WHITE)
T(d, (64, 186), 'ASICSの靴を、', font('Black', TITLE), DEEP)
T(d, (64, 306), '無料で借りられる', font('Black', TITLE), VIO)
d.rounded_rectangle((60, 460, 1020, 640), radius=32, fill=DEEP)
T(d, (540, 534), 'OneASICS会員か、ASICS公式LINEを', font('Black', 38), WHITE, 'ms')
T(d, (540, 596), '追加すると、利用時間中は無料', font('Black', 38), SUN, 'ms')
T(d, (540, 690), '通常は1足1時間550円（税込）', font('Medium', 34), DEEP, 'ms')
d.rounded_rectangle((60, 730, 1020, 1220), radius=40, fill=WHITE)
sh = shoe_illust(300); paste_c(im, sh, 255, 990)
d = ImageDraw.Draw(im)
T(d, (470, 830), '3モデルから選べる', font('Black', 40), DEEP, 'ls')
yy = 910
for kind, name in (('ピックルボールシューズ', 'GAME FF PICKLEBALL'), ('テニスシューズ', 'SOLUTION SPEED FF 4'), ('テニスシューズ', 'GEL-RESOLUTION X')):
    T(d, (470, yy), kind, font('Medium', 24), GREY, 'ls'); T(d, (470, yy + 40), name, font('Black', 32), NAVY, 'ls'); yy += 96
T(d, (1000, 1200), '※イラストはイメージです', font('Medium', 22), GREY, 'rs')
footer(d, 5, DEEP); im.save(f'{OUT}/05.png')

# ---------- 6 3モデル ----------
im, d, y = head('シューズ', ['借りられる', '3つのモデル'], [])
y -= 6
models = [
    (GAME, 0, 'GAME FF PICKLEBALL', 'ピックルボールシューズ', '軽くてやわらかい、スピード感を', '求める人向けのシューズ'),
    (SPEED, 0, 'SOLUTION SPEED FF 4', 'テニスシューズ', 'スピードと俊敏性を', '求める人向けのシューズ'),
    (RESO, 0, 'GEL-RESOLUTION X', 'テニスシューズ', '横の動きの安定性と', '快適性を追求したシューズ'),
]
rh = 214
for i, (img, side, name, kind, l1, l2) in enumerate(models):
    top = y + i * (rh + 16)
    d = shadow_card(im, (60, top, 1020, top + rh), r=30)
    d = ImageDraw.Draw(im)
    d.ellipse((110, top + rh / 2 - 56, 222, top + rh / 2 + 56), fill=CORAL if i == 0 else SEA)
    T(d, (166, top + rh / 2 + 4), str(i + 1), font('Black', 64), WHITE, 'mm')
    pill(d, 270, top + 26, kind, font('Black', 26), CORAL if i == 0 else SEA, WHITE, padx=16, pady=7)
    T(d, (270, top + 112), name, font('Black', 38), NAVY, 'ls')
    T(d, (270, top + 158), l1, font('Medium', 30), INK, 'ls')
    T(d, (270, top + 196), l2, font('Medium', 30), INK, 'ls')
T(d, (70, y + 3 * (rh + 16) + 30), 'サイズ：女性用22.5〜26.0cm／男性用24.5〜30.0cm（モデルにより異なる）', font('Medium', 25), GREY, 'ls')
footer(d, 6); im.save(f'{OUT}/06.png')

# ---------- 7 靴と道具の注意 ----------
im, d, y = head('注意', ['使える靴は、', 'NON-MARKINGだけ'], [])
d = shadow_card(im, (60, y, 1020, y + 290))
sx, sy = 160, y + 40
d.rounded_rectangle((sx, sy, sx + 760, sy + 110), radius=55, fill=(232, 234, 240), outline=(170, 176, 190), width=4)
for xx in range(sx + 70, sx + 700, 42): d.line([(xx, sy + 18), (xx - 14, sy + 92)], fill=(205, 208, 216), width=6)
pill(d, sx + 380, sy + 27, 'NON-MARKING', font('Black', 40), NAVY, WHITE, anchor='c', padx=26, pady=10)
T(d, (540, y + 210), '靴底にこの表示がある室内用の靴だけ使えます', font('Medium', 34), INK, 'ms')
T(d, (540, y + 258), 'ない人は、会場でレンタルを', font('Black', 34), CORAL, 'ms')
ry = y + 370
T(d, (70, ry), 'レンタルと購入（税込）', font('Black', 42), NAVY, 'ls')
end = rows(d, 80, ry + 84, [('シューズ', '1足1時間 550円（レンタル）'), ('パドル', '1本1時間 550円（レンタル）'), ('ボール', '1個 550円（購入）'), ('支払い', '会場ではキャッシュレスのみ')], kw=200, size=38, gap=72)
T(d, (80, end + 4), '※シューズは、OneASICS会員かASICS公式LINEの追加で無料', font('Medium', 28), CORAL, 'ls')
footer(d, 7); im.save(f'{OUT}/07.png')

# ---------- 8 予約＋CTA ----------
im = Image.new('RGB', (W, H), DEEP); d = ImageDraw.Draw(im)
pill(d, 70, 96, '予約', font('Black', 36), CORAL, WHITE)
T(d, (64, 186), '予約は、', font('Black', TITLE), WHITE)
T(d, (64, 306), 'もう受付中', font('Black', TITLE), SUN)
d.rounded_rectangle((60, 480, 1020, 860), radius=36, fill=WHITE)
yy = 568
items8 = (('予約', '「RESERVE ONE」で事前予約'), ('支払い', 'カードで事前決済（1時間単位）'), ('キャンセル', '3日前まで無料、2日前から全額'))
for i, (a_, b_) in enumerate(items8):
    T(d, (100, yy), a_, font('Black', 32), GREY, 'ls'); T(d, (300, yy), b_, font('Black', 38), NAVY, 'ls')
    if i < len(items8) - 1: d.line([(100, yy + 36), (980, yy + 36)], fill=(232, 226, 214), width=3)
    yy += 112
T(d, (70, 950), '予約ページは、プロフィールの', font('Medium', 46), WHITE)
T(d, (70, 1014), 'リンクのコート情報から', font('Medium', 46), WHITE)
pill(d, 70, 1090, 'pickleball-tokyo.com', font('Black', 36), SUN, DEEP, padx=24, pady=13)
T(d, (70, H - 56), 'PICKLEBALL TOKYO', font('Bold', 26), WHITE, 'ls')
T(d, (W - 70, H - 56), f'8/{N}  @pickleballtokyo', font('Medium', 26), WHITE, 'rs')
im.save(f'{OUT}/08.png')

th = [Image.open(f'{OUT}/0{i}.png').resize((360, 450)) for i in range(1, N + 1)]
sheet = Image.new('RGB', (360 * 4 + 50, 450 * 2 + 30), (200, 200, 200))
for i, t in enumerate(th): sheet.paste(t, (10 + (i % 4) * 370, 10 + (i // 4) * 460))
sheet.save(f'{OUT}/sheet.png')
