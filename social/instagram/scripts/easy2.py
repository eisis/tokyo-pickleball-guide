from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, sys
SP = '/tmp/claude-0/-home-claude/0fff00e8-7c5d-5fff-9e17-a4c63dd6bcc3/scratchpad/'
sys.path.insert(0, SP)
from art import paddle, ball as ball3d, place_ball
OUT = '/home/claude/ig-easy'; os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350; N = 7
F = '/usr/share/fonts/opentype/noto/NotoSansCJK-%s.ttc'
def font(w, s): return ImageFont.truetype(F % w, s, index=0)
NAVY = (14, 52, 82); SEA = (31, 127, 184); CORAL = (255, 107, 74); SUN = (255, 214, 120)
WHITE = (255, 255, 255); SAND = (246, 236, 216); INK = (30, 40, 50); GREY = (110, 118, 126); KIT = (24, 168, 150)
SKIN = (238, 192, 156); HAIR = (52, 38, 32); GRAYH = (205, 205, 210)
TITLE = 96; BODY = 46; LH = 70
def T(d, xy, s, f, c, a='la'): d.text(xy, s, font=f, fill=c, anchor=a)
def pill(d, x, y, s, f, bg, fg, padx=26, pady=13, anchor='l'):
    w = d.textlength(s, font=f); tw = w + padx * 2
    if anchor == 'c': x = x - tw / 2
    d.rounded_rectangle((x, y, x + tw, y + f.size + pady * 2), radius=(f.size + pady * 2) // 2, fill=bg)
    T(d, (x + padx, y + pady + f.size * 0.88), s, f, fg, 'ls')
    return x + tw
def footer(d, page, c=NAVY):
    T(d, (70, H - 56), 'PICKLEBALL TOKYO', font('Bold', 26), c, 'ls')
    T(d, (W - 70, H - 56), f'{page}/{N}  @pickleballtokyo', font('Medium', 26), c, 'rs')
def shadow_card(im, box, r=36, fill=WHITE):
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    x0, y0, x1, y1 = box
    sd.rounded_rectangle((x0 + 6, y0 + 14, x1 + 6, y1 + 14), radius=r, fill=(14, 52, 82, 40))
    sh = sh.filter(ImageFilter.GaussianBlur(14)); im.paste(sh, (0, 0), sh)
    d = ImageDraw.Draw(im); d.rounded_rectangle(box, radius=r, fill=fill); return d
def ghost(im, x, y, r, alpha):
    b = ball3d(r); b.putalpha(b.getchannel('A').point(lambda v: int(v * alpha)))
    im.paste(b, (int(x - b.width / 2), int(y - b.height / 2)), b)
def dashed(d, pts, color, width=6, dash=18, gap=14):
    acc = 0; on = True
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = math.hypot(x1 - x0, y1 - y0); t = 0
        while t < seg:
            step = min((dash if on else gap) - acc, seg - t)
            if on:
                a = t / seg; b = (t + step) / seg
                d.line([(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)], fill=color, width=width)
            t += step; acc += step
            if acc >= (dash if on else gap): acc = 0; on = not on
def bez(p0, p1, p2, n=60):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]
def arrow_head(d, pts, c, s=24):
    (x0, y0), (x1, y1) = pts[-4], pts[-1]; a = math.atan2(y1 - y0, x1 - x0)
    d.polygon([(x1 + s * math.cos(a), y1 + s * math.sin(a)), (x1 + s * math.cos(a + 2.5), y1 + s * math.sin(a + 2.5)), (x1 + s * math.cos(a - 2.5), y1 + s * math.sin(a - 2.5))], fill=c)

# ---------- 人物（2倍で描いて縮小。顔は描かない） ----------
class Fig:
    def __init__(self, w, h, k=3):
        self.k = k; self.im = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.im)
    def P(self, p): return (p[0] * self.k, p[1] * self.k)
    def limb(self, p, q, r1, r2, c):
        (x1, y1), (x2, y2) = self.P(p), self.P(q); r1 *= self.k; r2 *= self.k
        a = math.atan2(y2 - y1, x2 - x1); n = a + math.pi / 2
        self.d.polygon([(x1 + r1 * math.cos(n), y1 + r1 * math.sin(n)), (x2 + r2 * math.cos(n), y2 + r2 * math.sin(n)),
                        (x2 - r2 * math.cos(n), y2 - r2 * math.sin(n)), (x1 - r1 * math.cos(n), y1 - r1 * math.sin(n))], fill=c)
        self.d.ellipse((x1 - r1, y1 - r1, x1 + r1, y1 + r1), fill=c); self.d.ellipse((x2 - r2, y2 - r2, x2 + r2, y2 + r2), fill=c)
    def poly(self, pts, c): self.d.polygon([self.P(p) for p in pts], fill=c)
    def ell(self, box, c, outline=None, width=0):
        self.d.ellipse([v * self.k for v in box], fill=c, outline=outline, width=width * self.k)
    def rrect(self, box, r, c): self.d.rounded_rectangle([v * self.k for v in box], radius=r * self.k, fill=c)
    def chord(self, box, a0, a1, c): self.d.chord([v * self.k for v in box], a0, a1, fill=c)
    def paddle(self, hand, ang, L, c, rim=NAVY):
        # hand から角度 ang（度）の方向に、グリップ→面
        a = math.radians(ang); ux, uy = math.cos(a), math.sin(a)
        g1 = hand; g2 = (hand[0] + ux * L * 0.35, hand[1] + uy * L * 0.35)
        self.limb(g1, g2, L * 0.055, L * 0.055, rim)
        fc = (hand[0] + ux * L * 0.68, hand[1] + uy * L * 0.68)
        face = Image.new('RGBA', (int(L * 0.5 * self.k), int(L * 0.68 * self.k)), (0, 0, 0, 0)); fd = ImageDraw.Draw(face)
        fd.rounded_rectangle((0, 0, face.width - 1, face.height - 1), radius=int(face.width * 0.36), fill=rim)
        b = int(L * 0.04 * self.k)
        fd.rounded_rectangle((b, b, face.width - 1 - b, face.height - 1 - b), radius=int(face.width * 0.32), fill=c)
        fd.polygon([(b, face.height * 0.62), (face.width - b, face.height * 0.48), (face.width - b, face.height * 0.58), (b, face.height * 0.72)], fill=CORAL if c != CORAL else SUN)
        face = face.rotate(-(ang - 90) - 180, expand=True, resample=Image.BICUBIC)
        X, Y = self.P(fc); self.im.alpha_composite(face, (int(X - face.width / 2), int(Y - face.height / 2)))
    def arc(self, box, a0, a1, c, w): self.d.arc([v * self.k for v in box], a0, a1, fill=c, width=int(w * self.k))
    def face(self, cx, cy, r, side=0):
        # side=0 正面、1 右向き。点の目と、にっこり口、ほっぺ
        ink = (60, 40, 35); blush = (255, 160, 150)
        if side == 0:
            for sx in (-1, 1):
                self.ell((cx + sx * r * 0.36 - r * 0.1, cy + r * 0.02 - r * 0.12, cx + sx * r * 0.36 + r * 0.1, cy + r * 0.02 + r * 0.12), ink)
                self.ell((cx + sx * r * 0.58 - r * 0.15, cy + r * 0.32 - r * 0.09, cx + sx * r * 0.58 + r * 0.15, cy + r * 0.32 + r * 0.09), blush)
            self.arc((cx - r * 0.26, cy + r * 0.12, cx + r * 0.26, cy + r * 0.56), 20, 160, ink, r * 0.08)
        else:
            self.ell((cx + r * 0.5 - r * 0.1, cy - r * 0.02 - r * 0.12, cx + r * 0.5 + r * 0.1, cy - r * 0.02 + r * 0.12), ink)
            self.ell((cx + r * 0.38 - r * 0.15, cy + r * 0.32 - r * 0.09, cx + r * 0.38 + r * 0.15, cy + r * 0.32 + r * 0.09), blush)
            self.arc((cx + r * 0.45, cy + r * 0.18, cx + r * 0.9, cy + r * 0.56), 40, 140, ink, r * 0.08)
    def out(self): return self.im.resize((self.im.width // self.k, self.im.height // self.k), Image.LANCZOS)

def front_person(f, cx, fy, h, shirt, bottom, kind, pad_side=1, pad_c=SUN, collar=WHITE, trim=None):
    """正面の立ち姿。kind: child / woman / man / senior"""
    hr = h * (0.105 if kind == 'child' else 0.085)
    hy = fy - h + hr
    sw = h * (0.15 if kind == 'child' else 0.16)
    sh_y = hy + hr + h * 0.045; hip_y = fy - h * 0.46
    hair = GRAYH if kind == 'senior' else HAIR
    # 脚と靴
    long_pants = kind == 'senior'
    for s in (-1, 1):
        f.limb((cx + s * sw * 0.45, hip_y), (cx + s * sw * 0.55, fy - h * 0.04), h * 0.05, h * 0.04, bottom if long_pants else SKIN)
        f.rrect((cx + s * sw * 0.55 - h * 0.05 + s * h * 0.02, fy - h * 0.045, cx + s * sw * 0.55 + h * 0.05 + s * h * 0.02, fy + h * 0.01), h * 0.025, NAVY)
    # 下（スカート／ショーツ）
    if kind == 'woman':
        f.poly([(cx - sw * 0.85, hip_y - h * 0.05), (cx + sw * 0.85, hip_y - h * 0.05), (cx + sw * 1.15, hip_y + h * 0.13), (cx - sw * 1.15, hip_y + h * 0.13)], bottom)
        for j in range(1, 6):  # プリーツ
            t = j / 6
            xa = cx - sw * 0.85 + sw * 1.7 * t; xb = cx - sw * 1.15 + sw * 2.3 * t
            f.d.line([f.P((xa, hip_y - h * 0.02)), f.P((xb, hip_y + h * 0.13))], fill=tuple(max(0, v - 30) for v in bottom), width=int(h * 0.006 * f.k))
    elif not long_pants:
        f.poly([(cx - sw * 0.85, hip_y - h * 0.05), (cx + sw * 0.85, hip_y - h * 0.05), (cx + sw * 0.95, hip_y + h * 0.1), (cx + h * 0.01, hip_y + h * 0.1), (cx, hip_y + h * 0.04), (cx - h * 0.01, hip_y + h * 0.1), (cx - sw * 0.95, hip_y + h * 0.1)], bottom)
    else:
        f.poly([(cx - sw * 0.85, hip_y - h * 0.05), (cx + sw * 0.85, hip_y - h * 0.05), (cx + sw * 0.9, hip_y + h * 0.05), (cx - sw * 0.9, hip_y + h * 0.05)], bottom)
    # 腕（パドル側はひじを曲げて前に、反対は下ろす）
    # 腕：左右とも同じ長さで、ももの途中まで自然に下ろす
    for side in (-1, 1):
        sh = (cx + side * sw * 1.03, sh_y + h * 0.09)
        el = (cx + side * sw * 1.12, sh_y + h * 0.21)
        hd = (cx + side * sw * 1.2, hip_y + h * 0.06)
        f.limb(sh, el, h * 0.036, h * 0.032, SKIN); f.limb(el, hd, h * 0.032, h * 0.03, SKIN)
        if side == pad_side:
            hand = hd
    f.paddle(hand, 80 if pad_side > 0 else 100, h * 0.3, pad_c)
    # 胴と半袖を、ひと続きのシャツの形（1枚の多角形）で描く。袖は腕の向きに沿わせ、肩はなめらかな曲線に
    def half(side):
        S = (cx + side * sw * 1.0, sh_y + h * 0.06); E = (cx + side * sw * 1.12, sh_y + h * 0.21)
        dx, dy = E[0] - S[0], E[1] - S[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        nx, ny = uy * side, -ux * side  # 外向きの法線
        if nx * side < 0: nx, ny = -nx, -ny
        rs = h * 0.047
        M = (S[0] + dx * 0.5, S[1] + dy * 0.5)
        out_end = (M[0] + nx * rs, M[1] + ny * rs); in_end = (M[0] - nx * rs, M[1] - ny * rs)
        top = (cx + side * sw * 0.78, sh_y)
        shoulder = bez(top, (cx + side * sw * 1.12, sh_y - h * 0.004), out_end, n=16)
        return [(cx + side * nw * 1.15, sh_y)] + shoulder + [in_end, (cx + side * sw * 0.86, sh_y + h * 0.15), (cx + side * sw * 0.86, hip_y + h * 0.01)]
    nw = hr * 0.42
    r_ = half(1); l_ = half(-1)
    f.poly(r_ + list(reversed(l_)), shirt)
    # 首・頭・髪
    nw = hr * 0.42  # 首は頭の太さに合わせる
    f.rrect((cx - nw, hy + hr * 0.6, cx + nw, sh_y + h * 0.03), nw * 0.4, SKIN)
    pk = tuple(max(0, v - 25) for v in shirt)
    f.rrect((cx - nw * 0.32, sh_y + h * 0.035, cx + nw * 0.32, sh_y + h * 0.13), nw * 0.1, pk)
    for by_ in (0.07, 0.105): f.ell((cx - nw * 0.12, sh_y + h * by_ - nw * 0.12, cx + nw * 0.12, sh_y + h * by_ + nw * 0.12), collar)
    for sd_ in (-1, 1):
        f.poly([(cx + sd_ * nw * 1.45, sh_y - h * 0.008), (cx + sd_ * nw * 0.05, sh_y + h * 0.042), (cx + sd_ * nw * 0.95, sh_y + h * 0.078)], collar)
    if kind == 'woman':  # ポニーテール
        f.ell((cx + hr * 0.55, hy - hr * 0.2, cx + hr * 1.35, hy + hr * 1.3), hair)
    f.ell((cx - hr, hy - hr, cx + hr, hy + hr), SKIN)
    f.chord((cx - hr * 1.04, hy - hr * 1.08, cx + hr * 1.04, hy + hr * (0.5 if kind != 'senior' else 0.3)), 180, 360, hair)
    if kind in ('man', 'child'):
        f.chord((cx - hr * 1.04, hy - hr * 1.08, cx + hr * 1.04, hy + hr * 0.9), 160, 200, hair)
    if kind == 'woman':
        f.chord((cx - hr * 1.06, hy - hr * 1.08, cx + hr * 1.06, hy + hr * 1.1), 150, 210, hair)
        f.chord((cx - hr * 1.06, hy - hr * 1.08, cx + hr * 1.06, hy + hr * 1.1), 330, 390, hair)
    f.face(cx, hy + hr * 0.12, hr)
    # 帽子は正面向き：つばは額の前に、頭と同じ中心で横に広がる半楕円
    if kind == 'senior':  # サンバイザー（白いバンド＋つば）
        f.rrect((cx - hr * 1.04, hy - hr * 0.66, cx + hr * 1.04, hy - hr * 0.38), hr * 0.12, WHITE)
        f.d.chord([v * f.k for v in (cx - hr * 1.3, hy - hr * 0.7, cx + hr * 1.3, hy - hr * 0.1)], 0, 180, fill=WHITE, outline=(205, 212, 220), width=2 * f.k)
    if kind == 'child':  # 野球帽（丸いクラウン＋縫い目＋ボタン＋前に張り出したつば）
        CAP, CAPD = CORAL, (214, 74, 50)
        f.chord((cx - hr * 1.08, hy - hr * 1.16, cx + hr * 1.08, hy + hr * 0.36), 180, 360, CAP)
        f.d.line([f.P((cx, hy - hr * 1.12)), f.P((cx, hy - hr * 0.42))], fill=CAPD, width=int(hr * 0.07 * f.k))
        f.ell((cx - hr * 0.13, hy - hr * 1.24, cx + hr * 0.13, hy - hr * 1.0), CAPD)
        # つば：クラウンの右下から横に張り出す（根元はクラウンに重ねて、切れ目を作らない）
        f.d.chord([v * f.k for v in (cx - hr * 0.2, hy - hr * 0.62, cx + hr * 1.95, hy - hr * 0.1)], 0, 180, fill=CAPD)
        f.d.rectangle([v * f.k for v in (cx - hr * 1.06, hy - hr * 0.44, cx + hr * 1.06, hy - hr * 0.36)], fill=CAPD)

def server(f, x, fy, h):
    """横向き（右向き）で、腰より下からサーブを打つ人。6枚目の人と同じ作り（襟付きポロ・太めの首・顔あり）"""
    u = h / 520
    P = lambda a, b: (x + a * u, fy + b * u)
    SHIRT, COL, BOT = SUN, NAVY, NAVY
    head = P(18, -470); hr = 44 * u
    hip = P(-6, -252)
    kneeF, footF = P(58, -128), P(96, -10); kneeB, footB = P(-56, -122), P(-98, -24)
    # 奥の腕（胴のうしろ）
    f.limb(P(-12, -384), P(-40, -318), 17 * u, 15 * u, SKIN); f.limb(P(-40, -318), P(-50, -258), 15 * u, 14 * u, SKIN)
    f.limb(P(-12, -388), P(-26, -350), 24 * u, 22 * u, SHIRT)
    # 脚と靴
    f.limb(hip, kneeB, 24 * u, 20 * u, SKIN); f.limb(kneeB, footB, 20 * u, 16 * u, SKIN)
    f.rrect((footB[0] - 34 * u, footB[1] - 10 * u, footB[0] + 30 * u, footB[1] + 16 * u), 12 * u, NAVY)
    f.limb(hip, kneeF, 25 * u, 21 * u, SKIN); f.limb(kneeF, footF, 21 * u, 16 * u, SKIN)
    f.rrect((footF[0] - 30 * u, footF[1] - 12 * u, footF[0] + 40 * u, footF[1] + 14 * u), 12 * u, NAVY)
    # ショーツ
    f.poly([P(-48, -280), P(40, -280), P(52, -196), P(12, -190), P(-2, -214), P(-22, -188), P(-62, -198)], BOT)
    # 首（頭の太さに合わせる）
    f.limb(P(6, -396), P(14, -434), 19 * u, 19 * u, SKIN)
    # 胴（ポロ）：肩はなめらかな曲線、ひとつの形で
    shoulder = bez(P(-40, -372), P(-30, -414), P(4, -414), n=12) + bez(P(4, -414), P(36, -414), P(42, -372), n=12)
    f.poly(shoulder + [P(46, -300), P(46, -266), P(-50, -266), P(-50, -320)], SHIRT)
    # 襟（首の前に）
    f.poly([P(0, -414), P(34, -410), P(30, -392), P(14, -398)], COL)
    f.rrect((22 * u + x, -398 * u + fy, 30 * u + x, -360 * u + fy), 3 * u, tuple(max(0, v - 30) for v in SHIRT))
    # 頭・髪・顔
    f.ell((head[0] - hr, head[1] - hr, head[0] + hr, head[1] + hr), SKIN)
    f.chord((head[0] - hr * 1.05, head[1] - hr * 1.08, head[0] + hr * 1.05, head[1] + hr * 0.5), 180, 360, HAIR)
    f.chord((head[0] - hr * 1.05, head[1] - hr * 1.08, head[0] + hr * 1.05, head[1] + hr * 1.0), 150, 200, HAIR)
    f.face(head[0], head[1] + hr * 0.12, hr, side=1)
    # 手前の腕：袖から出て、腰より下で前へ振る
    sh = P(8, -384); elb = P(34, -298); hand = P(96, -210)
    f.limb(sh, elb, 17 * u, 15 * u, SKIN); f.limb(elb, hand, 15 * u, 14 * u, SKIN)
    # 袖（腕に沿った形。肩側は胴に重ねて継ぎ目を作らない）
    dx, dy = elb[0] - sh[0], elb[1] - sh[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    m = (sh[0] + dx * 0.45, sh[1] + dy * 0.45); rs0, rs1 = 25 * u, 22 * u
    top_ = (sh[0] - dx / L * 18 * u, sh[1] - dy / L * 18 * u)
    f.poly([(top_[0] + nx * rs0, top_[1] + ny * rs0), (m[0] + nx * rs1, m[1] + ny * rs1), (m[0] - nx * rs1, m[1] - ny * rs1), (top_[0] - nx * rs0, top_[1] - ny * rs0)], SHIRT)
    f.paddle(hand, 20, 200 * u, CORAL)
    return fy - 262 * u, P(230, -160)

# ---------- 1 表紙 ----------
im = Image.new('RGB', (W, H), SEA); d = ImageDraw.Draw(im)
pill(d, 70, 100, 'はじめての人へ', font('Black', 34), CORAL, WHITE)
T(d, (64, 196), '運動が苦手でも、', font('Black', 92), WHITE)
T(d, (58, 312), 'ピックルボール', font('Black', 128), SUN)
T(d, (64, 470), 'ってできる？', font('Black', 100), WHITE)
T(d, (70, 640), 'できる理由が、4つあります', font('Black', 48), WHITE)
# ボールのうしろに、なめらかな光の帯（太さと濃さがボールに向かって増える）
arc = bez((120, 1180), (250, 840), (540, 930), n=120)
sw_ = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); sdr = ImageDraw.Draw(sw_)
for i in range(len(arc) - 1):
    t = i / (len(arc) - 1)
    w = 2 + 44 * t ** 1.4; al = int(10 + 120 * t ** 1.2)
    (x0, y0), (x1, y1) = arc[i], arc[i + 1]
    sdr.line([(x0 * 2, y0 * 2), (x1 * 2, y1 * 2)], fill=(255, 255, 255, al), width=int(w * 2))
    sdr.ellipse((x1 * 2 - w, y1 * 2 - w, x1 * 2 + w, y1 * 2 + w), fill=(255, 255, 255, al))
sw_ = sw_.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2))
im.paste(sw_, (0, 0), sw_)
p = paddle(width=225, angle=28)
im.paste(p, (680, 1225 - p.height), p)
place_ball(im, 545, 930, 62)
# きらっと光る小さな星
d = ImageDraw.Draw(im)
def spark(x, y, r):
    d.polygon([(x, y - r), (x + r * 0.22, y - r * 0.22), (x + r, y), (x + r * 0.22, y + r * 0.22), (x, y + r), (x - r * 0.22, y + r * 0.22), (x - r, y), (x - r * 0.22, y - r * 0.22)], fill=SUN)
# 星はなし
d = ImageDraw.Draw(im); footer(d, 1, WHITE)
im.save(f'{OUT}/01.png')

# ---------- 理由スライドの共通部分 ----------
def reason(no, title_lines, body_lines):
    im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
    pill(d, 70, 96, f'理由 {no}', font('Black', 36), CORAL, WHITE)
    y = 186
    for t in title_lines:
        T(d, (64, y), t, font('Black', TITLE), NAVY); y += 120
    y += 14
    for b in body_lines:
        T(d, (70, y), b, font('Medium', BODY), INK); y += LH
    top = y + 34
    d = shadow_card(im, (60, top, 1020, 1230))
    return im, d, top

# ---------- 2 コートが小さい ----------
im, d, top = reason(1, ['コートが小さい'], ['バドミントンのダブルスと同じ広さで、', 'テニスコートの約3分の1。', '走り回らなくても、ボールに届きます。'])
cx = 540; s = 840 / 23.77
tw, th = 23.77 * s, 10.97 * s
tx0 = cx - tw / 2; ty0 = top + 100
T(d, (tx0, top + 74), 'テニスコート', font('Black', 34), GREY, 'ls')
d.rectangle((tx0, ty0, tx0 + tw, ty0 + th), fill=(214, 232, 242))
L = WHITE
d.rectangle((tx0, ty0, tx0 + tw, ty0 + th), outline=L, width=5)
for yy in (ty0 + 1.37 * s, ty0 + th - 1.37 * s): d.line([(tx0, yy), (tx0 + tw, yy)], fill=L, width=4)
for xx in (cx - 6.40 * s, cx + 6.40 * s): d.line([(xx, ty0 + 1.37 * s), (xx, ty0 + th - 1.37 * s)], fill=L, width=4)
d.line([(cx - 6.40 * s, ty0 + th / 2), (cx + 6.40 * s, ty0 + th / 2)], fill=L, width=4)
pw, ph = 13.41 * s, 6.10 * s; px0, py0 = cx - pw / 2, ty0 + (th - ph) / 2; kk = 2.13 * s
d.rectangle((px0, py0, px0 + pw, py0 + ph), fill=KIT)
d.rectangle((cx - kk, py0, cx + kk, py0 + ph), fill=(20, 140, 125))
d.rectangle((px0, py0, px0 + pw, py0 + ph), outline=WHITE, width=5)
for xx in (cx - kk, cx + kk): d.line([(xx, py0), (xx, py0 + ph)], fill=WHITE, width=4)
for a, b in ((px0, cx - kk), (cx + kk, px0 + pw)): d.line([(a, py0 + ph / 2), (b, py0 + ph / 2)], fill=WHITE, width=4)
d.line([(cx, ty0 - 10), (cx, ty0 + th + 10)], fill=NAVY, width=7)
lab_y = ty0 + th + 40
pill(d, cx, lab_y, 'ピックルボールコートは、約3分の1', font('Black', 40), KIT, WHITE, anchor='c')
T(d, (cx, 1205), '※公式の寸法から計算', font('Medium', 24), GREY, 'ms')
footer(d, 2); im.save(f'{OUT}/02.png')

# ---------- 3 ボールがゆっくり（テニスと比べる） ----------
im, d, top = reason(2, ['ボールがゆっくり'], ['軽いプラスチックのボールで、', 'テニスほど速く飛びません。', '目で追えて、ラリーが続きやすい。'])
h2 = (1230 - top) / 2
# 上段：テニス
ly = top + h2 / 2 + 24
T(d, (110, top + 70), 'テニス', font('Black', 40), GREY, 'ls')
for i, dy in enumerate((-30, 0, 30)):
    d.rounded_rectangle((260 + i * 60, ly + dy - 5, 768, ly + dy + 5), radius=5, fill=(205, 212, 218))
tb = (840, ly); r = 52
d.ellipse((tb[0] - r, tb[1] - r, tb[0] + r, tb[1] + r), fill=(205, 222, 70), outline=(170, 190, 50), width=4)
d.arc((tb[0] - r * 1.6, tb[1] - r * 0.9, tb[0] - r * 0.2, tb[1] + r * 0.9), -60, 60, fill=WHITE, width=7)
d.arc((tb[0] + r * 0.2, tb[1] - r * 0.9, tb[0] + r * 1.6, tb[1] + r * 0.9), 120, 240, fill=WHITE, width=7)
T(d, (970, top + 70), 'ビュン！', font('Black', 44), GREY, 'rs')
d.line([(110, top + h2), (970, top + h2)], fill=(232, 226, 214), width=3)
# 下段：ピックルボール（ラベルは左上、帯はその下、ボールは右）
ly2 = top + h2 + h2 / 2 + 20
T(d, (110, top + h2 + 70), 'ピックルボール', font('Black', 40), KIT, 'ls')
# 放物線：左下から上がり、x=680 で頂点、ボールは頂点を過ぎて落ちかけたところ
Y0 = top + h2 + 125; px_ = 620; a_ = (1195 - Y0) / (620 - 130) ** 2
arc = [(x, Y0 + a_ * (x - px_) ** 2) for x in range(130, 851, 6)]
bx, by = arc[-1]
sw_ = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); sdr = ImageDraw.Draw(sw_)
for i in range(len(arc) - 1):
    t = i / (len(arc) - 1); w = 2 + 30 * t ** 1.4; al = int(10 + 150 * t ** 1.2)
    (x0, y0), (x1, y1) = arc[i], arc[i + 1]
    sdr.line([(x0 * 2, y0 * 2), (x1 * 2, y1 * 2)], fill=(255, 200, 110, al), width=int(w * 2))
    sdr.ellipse((x1 * 2 - w, y1 * 2 - w, x1 * 2 + w, y1 * 2 + w), fill=(255, 200, 110, al))
sw_ = sw_.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2)); im.paste(sw_, (0, 0), sw_)
place_ball(im, bx, by, 58, glow=False)
d = ImageDraw.Draw(im)
T(d, (970, top + h2 + 70), 'ふわっ', font('Black', 44), CORAL, 'rs')
footer(d, 3); im.save(f'{OUT}/03.png')

# ---------- 4 サーブは下から ----------
im, d, top = reason(3, ['サーブは下から'], ['サーブは、腰より下で打つルール。', 'いきなり速いサーブは飛んできません。'])
fy = 1150
f = Fig(W, H)
waist, contact = server(f, 315, fy, 505)
im.paste(f.out(), (0, 0), f.out())
d = ImageDraw.Draw(im)
dashed(d, [(100, waist), (980, waist)], (200, 120, 100), width=5)
T(d, (975, waist + 52), '腰の高さ', font('Black', 36), CORAL, 'rs')
d.line([(110, fy + 4), (970, fy + 4)], fill=(232, 226, 214), width=5)
arc = bez((contact[0] + 10, contact[1]), (640, waist - 230), (900, waist - 110), n=120)
sw_ = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); sdr = ImageDraw.Draw(sw_)
for i in range(len(arc) - 1):
    t = i / (len(arc) - 1); w = 2 + 22 * t ** 1.3; al = int(20 + 160 * t ** 1.2)
    (x0, y0), (x1, y1) = arc[i], arc[i + 1]
    sdr.line([(x0 * 2, y0 * 2), (x1 * 2, y1 * 2)], fill=CORAL + (al,), width=int(w * 2))
    sdr.ellipse((x1 * 2 - w, y1 * 2 - w, x1 * 2 + w, y1 * 2 + w), fill=CORAL + (al,))
sw_ = sw_.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.5)); im.paste(sw_, (0, 0), sw_)
place_ball(im, arc[-1][0], arc[-1][1], 40, glow=False)
d = ImageDraw.Draw(im)
pill(d, 790, fy - 110, '下から打つ', font('Black', 40), CORAL, WHITE, anchor='c')
footer(d, 4); im.save(f'{OUT}/04.png')

# ---------- 5 キッチン ----------
im, d, top = reason(4, ['ネットの手前で、', 'スマッシュできない'], ['ネットの手前の「キッチン」では、', 'ノーバウンドで打てません。'])
# 半面を上から見た図（上がネット）。左に図、右に○×
s = 64; cw = 6.10 * s; ch = 6.70 * s; kk = 2.13 * s; cx0 = 110; cy0 = top + 120
d.rectangle((cx0, cy0, cx0 + cw, cy0 + ch), fill=KIT)
d.rectangle((cx0, cy0, cx0 + cw, cy0 + kk), fill=(246, 136, 56))
d.rectangle((cx0, cy0, cx0 + cw, cy0 + ch), outline=WHITE, width=6)
d.line([(cx0, cy0 + kk), (cx0 + cw, cy0 + kk)], fill=WHITE, width=5)
d.line([(cx0 + cw / 2, cy0 + kk), (cx0 + cw / 2, cy0 + ch)], fill=WHITE, width=5)
# ネット：網目の帯＋上の白いテープ＋両端のポール
ny0, ny1 = cy0 - 40, cy0 + 6
d.rectangle((cx0 - 24, ny0, cx0 + cw + 24, ny1), fill=(232, 238, 242))
for xx in range(int(cx0 - 24), int(cx0 + cw + 24), 14): d.line([(xx, ny0), (xx, ny1)], fill=(120, 140, 160), width=2)
for yy in range(int(ny0), int(ny1), 12): d.line([(cx0 - 24, yy), (cx0 + cw + 24, yy)], fill=(120, 140, 160), width=2)
d.rectangle((cx0 - 24, ny0 - 8, cx0 + cw + 24, ny0 + 4), fill=WHITE, outline=NAVY, width=2)
for xx in (cx0 - 34, cx0 + cw + 24): d.rounded_rectangle((xx, ny0 - 22, xx + 12, ny1 + 6), radius=4, fill=NAVY)
pill(d, cx0 + cw / 2, ny0 - 64, 'ネット', font('Black', 28), NAVY, WHITE, padx=20, pady=8, anchor='c')
T(d, (cx0 + cw / 2, cy0 + kk / 2 + 4), 'キッチン', font('Black', 40), WHITE, 'mm')
rx = cx0 + cw + 50
def mark(y, ok, l1, l2, c2):
    c = KIT if ok else CORAL
    d.ellipse((rx, y - 34, rx + 68, y + 34), fill=c)
    if ok: d.ellipse((rx + 15, y - 19, rx + 53, y + 19), outline=WHITE, width=9)
    else:
        d.line([(rx + 20, y - 14), (rx + 48, y + 14)], fill=WHITE, width=10); d.line([(rx + 48, y - 14), (rx + 20, y + 14)], fill=WHITE, width=10)
    T(d, (rx + 88, y - 6), l1, font('Black', 38), NAVY, 'ls')
    T(d, (rx + 88, y + 46), l2, font('Black', 38), c2, 'ls')
mark(cy0 + kk / 2 - 10, False, 'ここでは', 'ノーバウンドNG', CORAL)
mark(cy0 + kk + (ch - kk) / 2 - 10, True, 'ここからは', 'ノーバウンドOK', KIT)
# 図と説明をつなぐ点線
for yy in (cy0 + kk / 2, cy0 + kk + (ch - kk) / 2):
    dashed(d, [(cx0 + cw + 8, yy), (rx - 8, yy)], (190, 180, 165), width=4, dash=8, gap=8)
T(d, (540, 1200), '※キッチンに入るのはOK。バウンドした球なら打てます', font('Medium', 26), GREY, 'ms')
footer(d, 5); im.save(f'{OUT}/05.png')

# ---------- 6 どの世代でも ----------
im = Image.new('RGB', (W, H), SEA); d = ImageDraw.Draw(im)
pill(d, 70, 96, 'だから', font('Black', 36), CORAL, WHITE)
T(d, (64, 186), 'どの世代でも、', font('Black', TITLE), WHITE)
T(d, (64, 306), '一緒に楽しめる', font('Black', TITLE), SUN)
y = 456
for b in ['子どもからシニアまで、', '同じコートで一緒にプレーできます。']:
    T(d, (70, y), b, font('Medium', BODY), WHITE); y += LH
# 床（コート）
fy = 1150
d.rounded_rectangle((40, fy - 40, 1040, fy + 70), radius=30, fill=KIT)
d.line([(70, fy + 10), (1010, fy + 10)], fill=WHITE, width=5)
f = Fig(W, H)
xs = [180 + i * 240 for i in range(4)]  # 立ち位置は等間隔
# ウェア：サイトと同じ色（紺・コーラル・イエロー・白）で、背景の青とトーンをそろえる
front_person(f, xs[0], fy, 430, NAVY, WHITE, 'senior', pad_side=-1, pad_c=SUN, collar=WHITE)
front_person(f, xs[1], fy, 450, CORAL, WHITE, 'woman', pad_side=1, pad_c=SUN, collar=WHITE)
front_person(f, xs[2], fy, 470, SUN, NAVY, 'man', pad_side=1, pad_c=CORAL, collar=NAVY)
front_person(f, xs[3], fy, 320, WHITE, NAVY, 'child', pad_side=1, pad_c=CORAL, collar=CORAL)
o = f.out(); im.paste(o, (0, 0), o)
d = ImageDraw.Draw(im); footer(d, 6, WHITE)
im.save(f'{OUT}/06.png')

# ---------- 7 CTA ----------
im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
T(d, (64, 190), 'まずは、', font('Black', 100), WHITE)
T(d, (58, 316), '1回やってみよう', font('Black', 112), SUN)
y = 520
for b in ['初心者向けの体験会と、', '道具を借りられるコートは、', 'プロフィールのリンクから。']:
    T(d, (70, y), b, font('Medium', 50), WHITE); y += 76
pill(d, 70, y + 36, 'pickleball-tokyo.com', font('Black', 50), WHITE, NAVY, padx=36, pady=20)
by = 1050
d.rounded_rectangle((60, by, 1020, by + 150), radius=40, fill=SEA)
px, py = 130, by + 75
d.polygon([(px - 38, py), (px + 40, py - 34), (px + 16, py + 36)], fill=WHITE)
d.polygon([(px - 38, py), (px + 40, py - 34), (px + 2, py + 9)], fill=(210, 230, 245))
T(d, (200, py - 26), '運動が苦手な友達にも、', font('Black', 42), WHITE, 'lm')
T(d, (200, py + 28), '送ってみてね', font('Black', 42), SUN, 'lm')
p = paddle(width=170, angle=-22)
im.paste(p, (800, 600), p)
place_ball(im, 930, 590, 32)
d = ImageDraw.Draw(im); footer(d, 7, WHITE)
im.save(f'{OUT}/07.png')

th = [Image.open(f'{OUT}/0{i}.png').resize((360, 450)) for i in range(1, N + 1)]
sheet = Image.new('RGB', (360 * 4 + 50, 450 * 2 + 30), (200, 200, 200))
for i, t in enumerate(th): sheet.paste(t, (10 + (i % 4) * 370, 10 + (i // 4) * 460))
sheet.save(SP + 'easy_sheet.png')
