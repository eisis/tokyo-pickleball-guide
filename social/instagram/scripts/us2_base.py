from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os
SP = '/tmp/claude-0/-home-claude/0fff00e8-7c5d-5fff-9e17-a4c63dd6bcc3/scratchpad/'
OUT = '/home/claude/ig-usa'; os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350; N = 8
F = '/usr/share/fonts/opentype/noto/NotoSansCJK-%s.ttc'
def font(w, s): return ImageFont.truetype(F % w, s, index=0)
NAVY = (14, 52, 82); NAVY2 = (28, 72, 108); DEEP = (9, 34, 56); SEA = (31, 127, 184); CORAL = (255, 107, 74)
SUN = (255, 214, 120); WHITE = (255, 255, 255); PALE = (170, 205, 230); FOOT = (120, 155, 180); KIT = (24, 168, 150)

def new(bg):
    im = Image.new('RGB', (W, H), bg); return im, ImageDraw.Draw(im)
def T(d, xy, s, f, c, a='la'): d.text(xy, s, font=f, fill=c, anchor=a)
def pill(d, x, y, s, f, bg, fg, padx=24, pady=12):
    w = d.textlength(s, font=f)
    d.rounded_rectangle((x, y, x + w + padx * 2, y + f.size + pady * 2), radius=(f.size + pady * 2) // 2, fill=bg)
    T(d, (x + padx, y + pady + f.size * 0.88), s, f, fg, 'ls')
def footer(d, page, c=FOOT, note=None):
    if note:
        for i, l in enumerate(note.split('\n')):
            T(d, (70, 1196 + i * 30), l, font('Medium', 22), c)
    T(d, (70, H - 60), 'PICKLEBALL TOKYO', font('Bold', 24), c, 'ls')
    T(d, (W - 70, H - 60), f'{page}/{N}  @pickleballtokyo', font('Medium', 24), c, 'rs')
def taper(d, p, q, r1, r2, c):
    """太さが変わる手足（p側の半径r1、q側の半径r2）"""
    (x1, y1), (x2, y2) = p, q
    a = math.atan2(y2 - y1, x2 - x1); n = a + math.pi / 2
    pts = [(x1 + r1 * math.cos(n), y1 + r1 * math.sin(n)), (x2 + r2 * math.cos(n), y2 + r2 * math.sin(n)),
           (x2 - r2 * math.cos(n), y2 - r2 * math.sin(n)), (x1 - r1 * math.cos(n), y1 - r1 * math.sin(n))]
    d.polygon(pts, fill=c)
    d.ellipse((x1 - r1, y1 - r1, x1 + r1, y1 + r1), fill=c); d.ellipse((x2 - r2, y2 - r2, x2 + r2, y2 + r2), fill=c)
def glow_ball(im, x, y, r):
    g = Image.new('RGBA', im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse((x - r * 2.6, y - r * 2.6, x + r * 2.6, y + r * 2.6), fill=(255, 214, 120, 90))
    g = g.filter(ImageFilter.GaussianBlur(r * 0.9)); im.paste(g, (0, 0), g)
    d = ImageDraw.Draw(im)
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 226, 90), outline=(230, 180, 50), width=4)
    for dx, dy in [(-.35, -.3), (.35, -.35), (0, .15), (-.4, .45), (.4, .4)]:
        rr = r * 0.15; d.ellipse((x + dx * r - rr, y + dy * r - rr, x + dx * r + rr, y + dy * r + rr), fill=(230, 180, 50))
    return d

def athlete(im, c=WHITE, band=CORAL, paddle=CORAL, ox=0, oy=0, s=1.0):
    """ジャンプスマッシュのシルエット（架空の人物・顔なし）"""
    d = ImageDraw.Draw(im)
    P = lambda x, y: (ox + x * s, oy + y * s)
    R = lambda r: r * s
    head = P(700, 690); shF, shB = P(676, 784), P(776, 772); hipF, hipB = P(734, 968), P(800, 962)
    elbB, handB = P(842, 664), P(812, 566)          # ラケットを振り上げる腕
    elbF, handF = P(612, 730), P(560, 664)          # ボールを指す腕
    kneeF, footF = P(684, 1052), P(748, 1126)       # 前脚：引きつける
    kneeB, footB = P(842, 1088), P(866, 1214)       # 後ろ脚：伸ばす
    # パドル（振り上げた手の先）
    pad = Image.new('RGBA', (240, 400), (0, 0, 0, 0)); pd = ImageDraw.Draw(pad)
    pd.rounded_rectangle((30, 10, 210, 250), radius=44, fill=paddle)
    pd.rounded_rectangle((96, 240, 144, 380), radius=14, fill=DEEP)
    pad = pad.rotate(28, expand=True, resample=Image.BICUBIC)
    pad = pad.resize((int(pad.width * s), int(pad.height * s)))
    im.paste(pad, (int(handB[0] - pad.width * 0.62), int(handB[1] - pad.height * 0.93)), pad)
    d = ImageDraw.Draw(im)
    # 脚
    taper(d, hipB, kneeB, R(40), R(30), c); taper(d, kneeB, footB, R(30), R(20), c)
    taper(d, hipF, kneeF, R(42), R(32), c); taper(d, kneeF, footF, R(32), R(20), c)
    for f, ang in ((footF, 0), (footB, 0)):
        d.rounded_rectangle((f[0] - R(40), f[1] - R(16), f[0] + R(34), f[1] + R(20)), radius=int(R(14)), fill=c)
    # 胴（胸を張った形）
    d.polygon([shF, P(724, 760), shB, P(812, 870), hipB, hipF, P(704, 880)], fill=c)
    d.line([P(728, 940), P(806, 936)], fill=NAVY, width=int(R(6)))     # ショーツの境目
    # 腕
    taper(d, shB, elbB, R(30), R(24), c); taper(d, elbB, handB, R(24), R(18), c)
    taper(d, shF, elbF, R(30), R(24), c); taper(d, elbF, handF, R(24), R(16), c)
    # 首・頭・ヘッドバンド
    taper(d, P(708, 746), P(716, 770), R(20), R(22), c)
    d.ellipse((head[0] - R(46), head[1] - R(50), head[0] + R(46), head[1] + R(48)), fill=c)
    d.polygon([P(652, 664), P(748, 670), P(746, 690), P(652, 684)], fill=band)
    return d

def picto(im, c=WHITE, band=CORAL, paddle=CORAL, ox=0, oy=0, s=1.0):
    """ピクトグラム風のプレーヤー（架空の人物・顔なし）。左へ踏み込んでフォアハンドで打つ"""
    d = ImageDraw.Draw(im)
    P = lambda x, y: (ox + x * s, oy + y * s); R = lambda r: r * s
    head = P(686, 606)
    neck, hip = P(716, 690), P(792, 862)
    shF, shB = P(712, 712), P(738, 706)
    elbF, handF = P(640, 790), P(566, 806)
    elbB, handB = P(828, 700), P(884, 640)
    kneeF, footF = P(690, 962), P(648, 1080)
    kneeB, footB = P(884, 978), P(968, 1074)
    # 床の影
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.ellipse((P(600, 1080)[0], P(600, 1080)[1] - R(14), P(1010, 1080)[0], P(1010, 1080)[1] + R(18)), fill=(0, 0, 0, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(R(8))); im.paste(sh, (0, 0), sh); d = ImageDraw.Draw(im)
    # 後ろ側の腕・脚
    taper(d, shB, elbB, R(22), R(20), c); taper(d, elbB, handB, R(20), R(16), c)
    taper(d, hip, kneeB, R(30), R(24), c); taper(d, kneeB, footB, R(24), R(18), c)
    d.rounded_rectangle((footB[0] - R(10), footB[1] - R(16), footB[0] + R(50), footB[1] + R(14)), radius=int(R(12)), fill=c)
    # 胴
    taper(d, neck, hip, R(54), R(44), c)
    # 前脚
    taper(d, hip, kneeF, R(30), R(24), c); taper(d, kneeF, footF, R(24), R(18), c)
    d.rounded_rectangle((footF[0] - R(54), footF[1] - R(16), footF[0] + R(12), footF[1] + R(14)), radius=int(R(12)), fill=c)
    # パドル（手の先、左へ向けて振り抜く）
    pad = Image.new('RGBA', (140, 260), (0, 0, 0, 0)); pd = ImageDraw.Draw(pad)
    pd.rounded_rectangle((10, 6, 130, 170), radius=34, fill=paddle)
    pd.rounded_rectangle((52, 162, 88, 252), radius=12, fill=DEEP)
    pad = pad.rotate(70, expand=True, resample=Image.BICUBIC)
    pad = pad.resize((int(pad.width * s), int(pad.height * s)))
    im.paste(pad, (int(handF[0] - pad.width + R(46)), int(handF[1] - pad.height * 0.62)), pad); d = ImageDraw.Draw(im)
    # 打つ腕（手前）
    taper(d, shF, elbF, R(23), R(20), c); taper(d, elbF, handF, R(20), R(16), c)
    # 頭（胴から少し離す）とヘッドバンド
    d.ellipse((head[0] - R(46), head[1] - R(46), head[0] + R(46), head[1] + R(46)), fill=c)
    d.chord((head[0] - R(46), head[1] - R(46), head[0] + R(46), head[1] + R(46)), 200, 340, fill=c)
    d.rectangle((head[0] - R(46), head[1] - R(22), head[0] + R(46), head[1] - R(6)), fill=band)
    d.ellipse((head[0] - R(46), head[1] - R(46), head[0] + R(46), head[1] + R(46)), outline=c, width=1)
    return d
