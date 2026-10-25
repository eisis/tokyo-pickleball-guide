# 投稿9「仕事帰りに行ける、夜遅くまで開いている屋内コート5選」（7枚）
# 事実は各施設の公式サイト・公式発表で確認（2026-10-25）
# 使い方：python3 night.py 出力先フォルダ
from PIL import Image, ImageDraw, ImageFilter
import os, sys, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/ig-night'
os.makedirs(OUT, exist_ok=True)
src = open(os.path.join(HERE, 'easy2.py'), encoding='utf-8').read().split('# ---------- 1 表紙')[0]
src = src.replace("sys.path.insert(0, SP)", "").replace("OUT = '/home/claude/ig-easy'; os.makedirs(OUT, exist_ok=True)", "")
exec(src)
import items_svg as I
N = 7
SITE = os.path.abspath(os.path.join(HERE, '../../..'))
BG = {'本八幡': 'pickle-bang-theory.jpg', '新橋': 'pickleball-one-ginza.png', '池袋': 'sansan-ikebukuro.jpg',
      '品川': 'seibu-fast-shinagawa.png', '丸の内': 'asics-pickleball-connect-tokia.jpg'}


def faint_bg(name, fade=0.80):
    """コートの写真を全面に敷き、砂色を重ねてうすくする（文字のじゃまをしない）"""
    ph = Image.open(os.path.join(SITE, 'public/images/courts', name)).convert('RGB')
    r = max(W / ph.width, H / ph.height); ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1), Image.LANCZOS)
    x = (ph.width - W) // 2; y = (ph.height - H) // 2
    ph = ph.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(2))
    return Image.blend(ph, Image.new('RGB', (W, H), SAND), fade)
NIGHT = (18, 24, 58); NIGHT2 = (34, 44, 96); BLD = (28, 36, 80); BLD2 = (40, 50, 104); WIN = (255, 214, 120)


BAND = (38, 50, 110); LAB = (190, 198, 236); EDGE = (70, 84, 150)
ORDER = ['本八幡', '新橋', '池袋', '品川', '丸の内']


def photo_strip(im, PH, names, fade_from=0.35):
    n = len(names); sw = W / n
    for k, nm in enumerate(names):
        ph = Image.open(os.path.join(SITE, 'public/images/courts', BG[nm])).convert('RGB')
        zm, ccx, ccy = {'丸の内': (1.5, 1.0, 0.85)}.get(nm, (1.0, 0.5, 0.5))
        w = int(round(sw * (k + 1))) - int(round(sw * k))
        r = max(w / ph.width, PH / ph.height) * zm; ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1), Image.LANCZOS)
        ox, oy = int((ph.width - w) * ccx), int((ph.height - PH) * ccy)
        im.paste(ph.crop((ox, oy, ox + w, oy + PH)), (int(round(sw * k)), 0))
    d = ImageDraw.Draw(im)
    for k in range(1, n): d.line([(int(round(sw * k)), 0), (int(round(sw * k)), PH)], fill=NIGHT, width=4)
    grad = Image.new('L', (1, PH)); [grad.putpixel((0, yy), int(255 * max(0, (yy - PH * fade_from) / (PH * (1 - fade_from))) ** 1.2)) for yy in range(PH)]
    im.paste(Image.new('RGB', (W, PH), NIGHT), (0, 0), grad.resize((W, PH)))
    top = Image.new('L', (1, PH)); [top.putpixel((0, yy), int(140 * max(0, 1 - yy / 200))) for yy in range(PH)]
    im.paste(Image.new('RGB', (W, PH), NIGHT), (0, 0), top.resize((W, PH)))
    return ImageDraw.Draw(im)


def frosted(im, box, r=36, blur=18, tint=0.45):
    """文字の後ろだけ、すりガラスのようにぼかして暗くする"""
    x0, y0, x1, y1 = [int(v) for v in box]
    reg = im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(blur))
    reg = Image.blend(reg, Image.new('RGB', reg.size, NIGHT), tint)
    m = Image.new('L', reg.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, reg.width - 1, reg.height - 1), radius=r, fill=255)
    im.paste(reg, (x0, y0), m)
    ImageDraw.Draw(im).rounded_rectangle((x0, y0, x1, y1), radius=r, outline=(84, 98, 160), width=2)
    return ImageDraw.Draw(im)


def photo_tiles(im, y0, y1, names, gap=12, x0=60, x1=1020, r=22):
    """写真を角丸のタイルにして横一列に並べる（文字とは重ねない）"""
    n = len(names); tw = (x1 - x0 - gap * (n - 1)) / n; th = y1 - y0
    for k, nm in enumerate(names):
        ph = Image.open(os.path.join(SITE, 'public/images/courts', BG[nm])).convert('RGB')
        zm, ccx, ccy = {'丸の内': (1.5, 1.0, 0.85)}.get(nm, (1.0, 0.5, 0.5))
        w = int(tw); r_ = max(w / ph.width, th / ph.height) * zm
        ph = ph.resize((int(ph.width * r_) + 1, int(ph.height * r_) + 1), Image.LANCZOS)
        ox, oy = int((ph.width - w) * ccx), int((ph.height - th) * ccy)
        tile = ph.crop((ox, oy, ox + w, oy + th))
        m = Image.new('L', tile.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, th - 1), radius=r, fill=255)
        im.paste(tile, (int(x0 + k * (tw + gap)), y0), m)
    return ImageDraw.Draw(im)


def pin_icon(d, px, py, c, hole):
    d.ellipse((px, py, px + 30, py + 30), fill=c); d.polygon([(px + 3, py + 21), (px + 27, py + 21), (px + 15, py + 42)], fill=c)
    d.ellipse((px + 9, py + 9, px + 21, py + 21), fill=hole)


def skyline(im, y0, y1, seed=3):
    """夜のビル街（窓に明かり）"""
    d = ImageDraw.Draw(im); rnd = random.Random(seed)
    x = 0
    while x < W:
        w = rnd.randint(70, 150); h = rnd.randint(int((y1 - y0) * 0.35), y1 - y0)
        c = BLD if rnd.random() < 0.5 else BLD2
        d.rectangle((x, y1 - h, x + w - 6, y1), fill=c)
        for wy in range(y1 - h + 18, y1 - 14, 26):
            for wx in range(x + 12, x + w - 22, 22):
                if rnd.random() < 0.42:
                    d.rectangle((wx, wy, wx + 9, wy + 12), fill=WIN)
        x += w
    return d


def train_icon(d, x, y, s=1.0, c=NAVY):
    w, h = 44 * s, 52 * s
    d.rounded_rectangle((x, y, x + w, y + h), radius=10 * s, fill=c)
    d.rounded_rectangle((x + 6 * s, y + 8 * s, x + w - 6 * s, y + 24 * s), radius=4 * s, fill=WHITE)
    for cx in (x + 12 * s, x + w - 12 * s): d.ellipse((cx - 4 * s, y + 32 * s, cx + 4 * s, y + 40 * s), fill=WHITE)
    d.line([(x + 8 * s, y + h + 8 * s), (x + 14 * s, y + h)], fill=c, width=int(4 * s)); d.line([(x + w - 8 * s, y + h + 8 * s), (x + w - 14 * s, y + h)], fill=c, width=int(4 * s))


def clock_icon(d, x, y, r=24, c=NAVY):
    d.ellipse((x, y, x + 2 * r, y + 2 * r), outline=c, width=6)
    d.line([(x + r, y + r), (x + r, y + r * 0.45)], fill=c, width=6); d.line([(x + r, y + r), (x + r * 1.45, y + r * 1.2)], fill=c, width=6)


def shoe_icon(im, x, y, w=72):
    g, vw, vh = I.sneaker(upper='#FFFFFF', accent='#0E3452', tab='#FF6B4A')
    p = I.render(g, vw, vh, w); im.paste(p, (int(x), int(y)), p)


def timeline(d, x0, y, x1, close_h):
    """18時から26時までの帯。閉まる時間まで色をつける"""
    h0, h1 = 18, 26
    X = lambda hh: x0 + (x1 - x0) * (hh - h0) / (h1 - h0)
    d.rounded_rectangle((x0, y, x1, y + 26), radius=13, fill=(228, 224, 214))
    d.rounded_rectangle((x0, y, X(close_h), y + 26), radius=13, fill=CORAL)
    for hh in range(h0, h1 + 1, 2):
        lab = f'{hh}時' if hh <= 24 else f'{hh}時'
        T(d, (X(hh), y + 66), lab, font('Medium', 26), GREY, 'ms')
    T(d, (x0, y - 18), '18時に会社を出たら', font('Medium', 28), INK, 'ls')


# ---------- 1 表紙：5つのコートの写真を並べ、下に「場所と何時まで」の一覧 ----------
im = Image.new('RGB', (W, H), NIGHT); d = ImageDraw.Draw(im)
pill(d, 70, 92, '保存版', font('Black', 36), CORAL, WHITE)
fH = font('Black', 104)
T(d, (62, 196), '仕事帰りに', fH, WHITE); T(d, (62 + d.textlength('仕事帰りに', font=fH), 196), '行ける', fH, SUN)
f2 = font('Black', 62)
T(d, (66, 330), 'ピックルボールコート', f2, WHITE); T(d, (66 + d.textlength('ピックルボールコート', font=f2) + 8, 330), '5選', f2, SUN)
T(d, (70, 458), '夜遅くまで開いている、駅近の屋内コート', font('Bold', 34), LAB, 'ls')
d = photo_tiles(im, 492, 640, ORDER)
T(d, (1020, 670), '写真：各施設', font('Medium', 22), LAB, 'rs')
# 一覧（帯と同じ夜の青）
ty = 690
d.rounded_rectangle((60, ty, 1020, 1230), radius=40, fill=BAND, outline=EDGE, width=2)
T(d, (152, ty + 60), '場所', font('Bold', 28), LAB, 'ls'); pin_icon(d, 108, ty + 30, LAB, BAND)
clock_icon(d, 720, ty + 28, 20, LAB); T(d, (772, ty + 60), '何時まで', font('Bold', 28), LAB, 'ls')
rows_ = [('本八幡', '25:00'), ('新橋', '23:00'), ('池袋', '23:00'), ('品川', '22:00'), ('丸の内', '22:00')]
yy = ty + 142
for k, (a_, t_) in enumerate(rows_):
    T(d, (108, yy), a_, font('Black', 52), WHITE, 'ls')
    T(d, (900, yy), t_, font('Black', 56), SUN, 'rs'); T(d, (912, yy), 'まで', font('Black', 30), WHITE, 'ls')
    if k < 4: d.line([(108, yy + 28), (972, yy + 28)], fill=EDGE, width=2)
    yy += 88
T(d, (70, H - 56), 'PICKLEBALL TOKYO', font('Bold', 26), WHITE, 'ls')
T(d, (W - 70, H - 56), f'1/{N}  @pickleballtokyo', font('Medium', 26), WHITE, 'rs')
im.save(f'{OUT}/01.png')

# ---------- 2〜6 各コート ----------
# 借りられるもの：(名前, 値段)。値段はすべて各施設の公式の表記どおり（税込）
courts = [
    ('本八幡', 'THE PICKLE BANG THEORY', ['THE PICKLE', 'BANG THEORY'], '25:00', 25, 'JR本八幡駅 北口から徒歩1分', False,
     [('パドル', '1本500円')], 'シューズの貸し出しはなし（ノーマーキングを持参）', '年中無休・男女別の更衣室あり'),
    ('新橋', 'ピックルボールワン銀座新橋', ['ピックルボールワン', '銀座新橋'], '23:00', 23, '新橋駅から地下通路で行ける', True,
     [('シューズ', '1時間500円'), ('パドル', '1時間500円')], '', '年中無休（年末年始は休み）'),
    ('池袋', 'Sansanピックルボールコート池袋', ['Sansanピックルボール', 'コート池袋'], '23:00', 23, '東池袋駅 6番出口から徒歩3分', True,
     [('シューズ', '1時間500円'), ('パドル', '1時間500円')], 'ウェア（Tシャツ・パンツ）も各500円で借りられる', '更衣室とシャワー室あり'),
    ('品川', 'SEIBU FAST SPORTS FIELD 品川', ['SEIBU FAST', 'SPORTS FIELD 品川'], '22:00', 22, '品川駅 高輪口から徒歩2分', True,
     [('シューズ', '1回500円'), ('パドル', '1回500円')], '', '品川プリンスホテル メインタワー10階'),
    ('丸の内', 'ASICS PICKLEBALL CONNECT', ['ASICS PICKLEBALL', 'CONNECT'], '22:00', 22, 'JR東京駅 丸の内南口から徒歩3分', True,
     [('シューズ', '1時間550円'), ('パドル', '1時間550円')], 'シューズはOneASICS会員か公式LINEの追加で無料', '10/31〜12/27の期間限定'),
]
for i, (area, full, lines, close, ch, access, rent, shoe, sub, note) in enumerate(courts):
    page = i + 2
    # 上半分：コートの写真を大きく。下に向かって夜の紺に溶けるグラデーション
    PH = 600
    zm, ccx, ccy = {'丸の内': (1.5, 1.0, 0.85)}.get(area, (1.0, 0.5, 0.5))
    im = Image.new('RGB', (W, H), NIGHT)
    ph = Image.open(os.path.join(SITE, 'public/images/courts', BG[area])).convert('RGB')
    r = max(W / ph.width, PH / ph.height) * zm; ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1), Image.LANCZOS)
    ox, oy = int((ph.width - W) * ccx), int((ph.height - PH) * ccy)
    ph = ph.crop((ox, oy, ox + W, oy + PH))
    im.paste(ph, (0, 0))
    grad = Image.new('L', (1, PH)); [grad.putpixel((0, yy), int(255 * max(0, (yy - PH * 0.25) / (PH * 0.75)) ** 1.3)) for yy in range(PH)]
    grad = grad.resize((W, PH)); top_shade = Image.new('L', (1, PH)); [top_shade.putpixel((0, yy), int(150 * max(0, 1 - yy / 220))) for yy in range(PH)]
    im.paste(Image.new('RGB', (W, PH), NIGHT), (0, 0), grad)
    im.paste(Image.new('RGB', (W, PH), NIGHT), (0, 0), top_shade.resize((W, PH)))
    d = ImageDraw.Draw(im)
    pill(d, 70, 92, f'{i + 1}/5', font('Black', 34), CORAL, WHITE)
    cr = '画像：ASICS（イメージ）' if area == '丸の内' else '写真：施設'
    cwd = d.textlength(cr, font=font('Medium', 22))
    d.rounded_rectangle((1010 - cwd - 24, 106, 1022, 142), radius=18, fill=NIGHT)
    T(d, (1010, 133), cr, font('Medium', 22), WHITE, 'rs')
    # コート名（写真の下のほう、白で）
    y = 364
    for ln in lines:
        f_ = font('Black', 80)
        assert d.textlength(ln, font=f_) < 950, ln
        T(d, (64, y), ln, f_, WHITE); y += 98
    # 閉まる時間：黄色の大きな帯
    top = 592
    BAND = (38, 50, 110); LAB = (190, 198, 236)
    d.rounded_rectangle((60, top, 1020, top + 224), radius=40, fill=BAND, outline=(70, 84, 150), width=2)
    # 左：場所（ピンのアイコン＋エリア名）
    px, py = 108, top + 52
    d.ellipse((px, py, px + 30, py + 30), fill=LAB); d.polygon([(px + 3, py + 21), (px + 27, py + 21), (px + 15, py + 42)], fill=LAB)
    d.ellipse((px + 9, py + 9, px + 21, py + 21), fill=BAND)
    T(d, (152, top + 82), '場所', font('Bold', 30), LAB, 'ls')
    T(d, (104, top + 184), area, font('Black', 80), WHITE, 'ls')
    d.line([(470, top + 40), (470, top + 184)], fill=(70, 84, 150), width=3)
    # 右：何時まで（時間だけ黄色）
    clock_icon(d, 510, top + 50, 21, LAB)
    T(d, (566, top + 82), '何時まで', font('Bold', 30), LAB, 'ls')
    fT, fM = font('Black', 112), font('Black', 48)
    tw = d.textlength(close, font=fT) + 10 + d.textlength('まで', font=fM)
    tx0 = 990 - tw
    T(d, (tx0, top + 192), close, fT, SUN, 'ls')
    T(d, (tx0 + d.textlength(close, font=fT) + 10, top + 192), 'まで', fM, WHITE, 'ls')
    assert tx0 > 500, (area, tx0)
    # 駅とシューズ
    top2 = top + 248
    d.rounded_rectangle((60, top2, 1020, top2 + 356), radius=36, fill=WHITE)
    train_icon(d, 112, top2 + 50, 1.0)
    T(d, (186, top2 + 70), '駅から', font('Medium', 28), GREY, 'ls')
    T(d, (186, top2 + 118), access, font('Black', 40), NAVY, 'ls')
    d.line([(110, top2 + 162), (970, top2 + 162)], fill=(232, 226, 214), width=3)
    T(d, (110, top2 + 214), '借りられるもの', font('Medium', 28), GREY, 'ls')
    if rent:
        pill(d, 330, top2 + 180, '手ぶらOK', font('Black', 28), KIT, WHITE, padx=18, pady=7)
    cx = 110
    for nm, pr in shoe:  # 名前は濃い色の札、値段は白い札で横に並べる
        fN, fP = font('Black', 32), font('Black', 32)
        wn = d.textlength(nm, font=fN) + 36; wp = d.textlength(pr, font=fP) + 36
        d.rounded_rectangle((cx, top2 + 238, cx + wn + wp, top2 + 294), radius=16, fill=SEA)
        d.rounded_rectangle((cx + wn, top2 + 241, cx + wn + wp - 3, top2 + 291), radius=13, fill=WHITE)
        d.rectangle((cx + wn, top2 + 241, cx + wn + 14, top2 + 291), fill=WHITE)
        T(d, (cx + 18, top2 + 278), nm, fN, WHITE, 'ls'); T(d, (cx + wn + 18, top2 + 278), pr, fP, SEA, 'ls')
        cx += wn + wp + 16
        assert cx < 1000, (area, cx)
    if sub:
        T(d, (110, top2 + 336), sub, font('Medium', 28), INK, 'ls')
    T(d, (540, 1240), note, font('Bold', 30), WHITE, 'ms')
    footer(d, page, WHITE); im.save(f'{OUT}/0{page}.png')

# ---------- 7 CTA ----------
im = Image.new('RGB', (W, H), NIGHT); d = ImageDraw.Draw(im)
T(d, (64, 196), '今週、仕事帰りに', font('Black', 92), WHITE)
T(d, (58, 316), '1回行ってみよう', font('Black', 104), SUN)
d = photo_tiles(im, 470, 620, ORDER)
T(d, (1020, 650), '写真：各施設', font('Medium', 22), LAB, 'rs')
by = 690
d.rounded_rectangle((60, by, 1020, by + 270), radius=40, fill=BAND, outline=EDGE, width=2)
T(d, (110, by + 74), '営業時間や予約の方法は、', font('Bold', 40), WHITE, 'ls')
T(d, (110, by + 128), 'プロフィールのリンクの各コートのページから', font('Bold', 34), WHITE, 'ls')
pill(d, 110, by + 160, 'pickleball-tokyo.com', font('Black', 40), SUN, NIGHT, padx=26, pady=13)
cy = 990
d.rounded_rectangle((60, cy, 1020, cy + 150), radius=40, fill=WHITE)
fC = font('Black', 42); l1 = '一緒に行けそうな同僚に、'
T(d, (110, cy + 92), l1, fC, NAVY, 'ls'); T(d, (110 + d.textlength(l1, font=fC), cy + 92), '送ってみてね', fC, CORAL, 'ls')
T(d, (70, 1206), '※営業時間や料金は変わることがあります。行く前に各施設の公式サイトで確認してください', font('Medium', 22), LAB, 'ls')
T(d, (70, H - 56), 'PICKLEBALL TOKYO', font('Bold', 26), WHITE, 'ls')
T(d, (W - 70, H - 56), f'7/{N}  @pickleballtokyo', font('Medium', 26), WHITE, 'rs')
im.save(f'{OUT}/07.png')

th = [Image.open(f'{OUT}/0{i}.png').resize((360, 450)) for i in range(1, N + 1)]
sheet = Image.new('RGB', (360 * 4 + 50, 450 * 2 + 30), (200, 200, 200))
for i, t in enumerate(th): sheet.paste(t, (10 + (i % 4) * 370, 10 + (i // 4) * 460))
sheet.save(f'{OUT}/sheet.png')
